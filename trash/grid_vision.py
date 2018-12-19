# can_see = True
# x = int(self.x / one_square)
# X = int(o.x / one_square)
# y = int(self.y / one_square)
# Y = int(o.y / one_square)
# diff_x = abs(X - x)
# diff_y = abs(Y - y)
# clearance_x = None
# clearance_y = None
#
# if not diff_y:
#     clearance_x = range(x + 1, X - 1) if x < X else range(X + 1, x - 1)
#     space_y = y
#     for space_x in clearance_x:
#         if grid[space_x, space_y] == 'Wall':
#             can_see = False
#             break
# elif not diff_x:
#     clearance_y = range(y + 1, Y - 1) if y < Y else range(Y + 1, y - 1)
#     space_x = x
#     for space_y in clearance_y:
#         if grid[space_x, space_y] == 'Wall':
#             can_see = False
#             break
# else:
#     clearance_x = range(x + 1, X - 1) if x < X else range(X + 1, x - 1)
#     clearance_y = range(y + 1, Y - 1) if y < Y else range(Y + 1, y - 1)
#     for space_x in clearance_x:
#         for space_y in clearance_y:
#             if grid[space_x, space_y] == 'Wall':
#                 can_see = False
#             if not can_see:
#                 break
#         if not can_see:
#             break
# if can_see: