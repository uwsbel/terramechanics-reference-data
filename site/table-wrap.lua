-- Every table on every page goes in a box that scrolls sideways when the table is wider than the text column
-- (site/site.css, .table-wrap), so a wide table never runs under the page's table of contents or widens the page.
-- A filter rather than the page generator, so the tables of the pages copied from docs/ get the box too
-- (2026-11-19, Dan's look at the soils page; tools/check_site_layout.py checks the result).
--
-- Column widths (2026-11-20, Dan: "the column width distribution ... seems to be an ever present issue"). Left to the
-- browser, a table's columns are sized by their longest unbreakable content, and browsers differ in how they share
-- what does not fit; a blanket minimum width per column (site.css, until 2026-11-20) made a two-character column as
-- wide as a long text column. The widths are set here from the content instead, the same in every browser: each
-- column's share is its preferred width in characters (its longest cell, capped at CAP so long text wraps, and never
-- less than its longest word), and the table is as wide as the text column, or wider, scrolling in its box, when the
-- columns do not fit side by side at their least widths (a column's longest word; on a phone, TEXT_MIN for a text
-- column).
-- Tables that set their own widths (the virtual experiment card, .vx-card) are left alone.

local CAP = 28        -- characters: a column with longer cells wraps rather than taking more of the table
local TEXT_MIN = 20   -- characters a column of longer text keeps at the least (16 gave 118 px, under the check's 7em),
                      -- so on a phone it scrolls sideways rather than wrapping to a word per line
                      -- (tools/check_site_layout.py: 'squeezed')
local PAD = 2         -- characters of cell padding (0.5rem each side, about one character)

-- the longest piece of a cell that cannot break: words, and the pieces of a long code between the break points the
-- page generator gives it after `_`, `;` and `,` (tools/build_site.py, table())
local function longest_piece(s)
  local m = 0
  for word in s:gmatch("%S+") do
    for piece in (word .. "_"):gmatch("([^_;,]*[_;,]?)") do
      local n = utf8.len(piece) or #piece
      if n > m then m = n end
    end
  end
  return m
end

local function widths(t)
  local n = #t.colspecs
  local longest, piece = {}, {}
  for i = 1, n do longest[i], piece[i] = 0, 0 end
  local function scan(rows)
    for _, row in ipairs(rows) do
      local col = 1
      for _, cell in ipairs(row.cells) do
        if col > n then break end
        local s = pandoc.utils.stringify(cell.contents)
        if (cell.col_span or 1) == 1 then   -- a cell spanning columns says nothing about one column's width
          longest[col] = math.max(longest[col], utf8.len(s) or #s)
          piece[col] = math.max(piece[col], longest_piece(s))
        end
        col = col + (cell.col_span or 1)
      end
    end
  end
  scan(t.head.rows)
  for _, b in ipairs(t.bodies) do scan(b.head); scan(b.body) end
  scan(t.foot.rows)
  local pref, total_pref, total_min, total_phone = {}, 0, 0, 0
  for i = 1, n do
    pref[i] = math.max(piece[i], math.min(longest[i], CAP)) + PAD
    total_pref = total_pref + pref[i]
    total_min = total_min + piece[i] + PAD
    total_phone = total_phone + math.max(piece[i], math.min(longest[i], TEXT_MIN)) + PAD
  end
  if total_pref == 0 then return t, nil end
  for i = 1, n do
    t.colspecs[i] = {t.colspecs[i][1], pref[i] / total_pref}
  end
  -- the table is as wide as the text column (Bootstrap's .table), and at least as wide as the columns' least widths
  -- need side by side (the box then scrolls): the longest pieces on a wide screen, and TEXT_MIN for a text column on
  -- a phone (applied on desktop too, it made the record pages' setup table scroll at 1280 px). Variables on the box,
  -- read by site.css, since Quarto's HTML pass drops a style on the table itself
  return t, string.format("--table-min: %dch; --table-min-phone: %dch", total_min, total_phone)
end

return {
  {
    -- the card's tables keep the widths site.css gives them (.vx-card); mark them before the widths pass
    Div = function(d)
      if d.classes:includes("vx-card") then
        d = d:walk({Table = function(t) t.attr.classes:insert("own-widths"); return t end})
      end
      return d
    end
  },
  {
    Table = function(t)
      local style
      if not t.attr.classes:includes("own-widths") then
        t, style = widths(t)
      end
      return pandoc.Div({t}, pandoc.Attr("", {"table-wrap"}, style and {style = style} or {}))
    end
  }
}
