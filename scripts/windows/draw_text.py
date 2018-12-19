import pygame as pg

from scripts.windows.text_windows.messages import message_dict


adj = 10
lineSpacing = -2


# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def draw_text(screen, message_name, color, rect, font_name, aa=False, bkg=None):
    rect = pg.Rect(rect)
    y = rect.top
    font = pg.font.SysFont(font_name, 30)
    # get the height of the font
    fontHeight = font.size("Tg")[1]
    if message_name in message_dict:
        text = message_dict[message_name]
    else:
        text = ''

    if bkg:
        rect_box = (int(rect[0]) - adj / 2, int(rect[1]) - adj / 2, int(rect[2]) + adj, int(rect[3]) + adj)
        # blit the rectangle
        pg.draw.rect(screen, bkg, rect_box, 0)
        pg.draw.rect(screen, color, rect_box, 2)

    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        new_line = 0
        while font.size(text[:i])[0] < rect.width and i < len(text) and not new_line:
            i += 1
            if 0 <= i + 2 < len(text):
                if text[i] == "/":
                    esc_statement = text[i + 1] + text[i + 2]
                    if esc_statement == "br":
                        new_line = 3
                        text = text[:i] + text[(3 + i):]

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            first_space = text.rfind(" ", 0, i + new_line)
            if first_space == -1:
                text = text[:i - 1] + "-" + text[i:]
            else:
                i = first_space + 1

        # render the line and blit it to the screen
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            # image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        # blit the text
        screen.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]
    return text
