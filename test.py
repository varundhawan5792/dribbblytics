from sklearn.cluster import KMeans
import colorsys
import json

def get_hsv(hexrgb):
    hexrgb = hexrgb.lstrip("#")   # in case you have Web color specs
    r, g, b = (int(hexrgb[i:i+2], 16) / 255.0 for i in xrange(0, 5, 2))
    return colorsys.rgb_to_hsv(r, g, b)


def get_rgb(hexrgb):
    hexrgb = hexrgb.lstrip("#")   # in case you have Web color specs
    split = (hexrgb[0:2], hexrgb[2:4], hexrgb[4:6])
    return [int(x, 16) for x in split]

colors = ["#030303", "#262626", "#5C5C5C", "#606060", "#A1A1A1", "#A7A7A7", "#F2F2F2", "#FDFDFD", "#FEFEFE", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#F8F7F7", "#231F1F", "#322626", "#CE6666", "#9A5E5D", "#F46E6B", "#E63F3A", "#FF605B", "#A1706E", "#997371", "#D95850", "#CF3329", "#E96F65", "#D7BEBB", "#C9C1C0", "#DB7769", "#A44133", "#DA7769", "#C84934", "#97554A", "#E2DCDB", "#D76653", "#D75D48", "#A29390", "#B2ADAC", "#AA6D5F", "#877672", "#88584C", "#C68C7C", "#4C3E3A", "#897670", "#DE572B", "#D67C5E", "#D1B6AD", "#CFA89B", "#B25738", "#E1D2CC", "#B98A77", "#E59676", "#866152", "#B9ADA8", "#9E908A", "#B6A096", "#543E34", "#C76C42", "#DCB19D", "#DB8155", "#99522F", "#F2F0EF", "#D1A086", "#613A24", "#F1A275", "#D88F65", "#E3854E", "#A7968C", "#F26F21", "#F6F1EE", "#B4AAA4", "#EEDACE", "#CCB5A7", "#E18A54", "#CF8B5F", "#8D7361", "#8E4614", "#A57350", "#DECDC1", "#5D524A", "#967257", "#E6741C", "#F3B989", "#734A28", "#BD8C63", "#EFB686", "#9C8773", "#F7EFE7", "#865E36", "#BF9C78", "#71512F", "#E2A65C", "#DACEBF", "#D2CCC4", "#E9E6E2", "#F7C178", "#9A6B2A", "#C8C1B7", "#BBB2A5", "#DC9E42", "#8F6E3D", "#D3D1CE", "#F8ECDA", "#C5964F", "#F39C14", "#8E744B", "#EC9E1F", "#D8CAB3", "#574525", "#B3AEA5", "#DDAB50", "#F5DAA8", "#564F42", "#D4AE67", "#D1B98C", "#D9B570", "#EBEAE8", "#E4CC9B", "#CDBA93", "#FBAA01", "#F5A908", "#E5D6B6", "#E8D19F", "#E3D3AF", "#EBE1C9", "#E5D4A6", "#A09C91", "#EDEAE1", "#DDB843", "#A49565", "#EFDEA6", "#F0D57C", "#ECEAE3", "#FCE388", "#F3F2EE", "#F6F5F1", "#DBD2A7", "#C2B14E", "#D4CEAA", "#CBC9BC", "#A39A40", "#DAD6AE", "#FFFBCA", "#FBF9E0", "#F2E105", "#C9C7AD", "#EAE9D2", "#EEEEED", "#48483D", "#E5E5BD", "#B1B372", "#EDEECE", "#A1A384", "#B1B941", "#A7B722", "#B4B7A8", "#ACCE45", "#D9DCD0", "#D4DDBC", "#D8E1C2", "#FAFBF8", "#5D8C1D", "#BFC9BA", "#717370", "#8ECA73", "#ABC0A2", "#87C76E", "#81B76C", "#7B8977", "#8BA085", "#6EA262", "#67A75E", "#A4AEA3", "#378C36", "#EDEEED", "#A7A8A7", "#5F8260", "#599361", "#85BE8D", "#4A7551", "#A7C6AF", "#97CCA6", "#A0C4AD", "#9CCFB2", "#8AAF9C", "#325745", "#79C9A8", "#222927", "#BACBC7", "#525D5B", "#4DC8B2", "#5DC2B0", "#70918C", "#94B4B0", "#40A297", "#3B5351", "#4FB3AF", "#2BA7A3", "#AACAC9", "#BDE1E0", "#2F5352", "#FEFFFF", "#FBFCFC", "#F8F9F9", "#EEEFEF", "#EBECEC", "#F7FAFA", "#EFF2F2", "#B1B5B5", "#373E3E", "#719191", "#BCDBDC", "#93DEE1", "#1BBEC5", "#5CCCD1", "#23474B", "#B6C6C8", "#779094", "#52A2B0", "#1A5863", "#A6DDE7", "#94BEC6", "#F3FDFF", "#1EB0CF", "#5FC6DF", "#65858D", "#0AA4CE", "#102D35", "#4CA7C1", "#57AFC9", "#4EB0CD", "#69919D", "#41555C", "#B1CED9", "#69828C", "#249FD4", "#7CB5CE", "#A4BCC7", "#0C6D9B", "#263D48", "#7495A5", "#F7F9FA", "#141617", "#F9FBFC", "#1B88BF", "#0773AA", "#58AEDB", "#22A5EB", "#3488B8", "#3488B8", "#5BA9D6", "#5E6366", "#568EB0", "#5088AA", "#949DA3", "#B5D0E2", "#121517", "#5895BF", "#5390BA", "#93B7D0", "#5B88A8", "#41484D", "#437CA5", "#0176CB", "#949FA7", "#2D6E9E", "#246EA5", "#7F8386", "#276EA4", "#3A434A", "#4198DC", "#ADBBC6", "#3B454D", "#BEC3C7", "#BEC3C7", "#4196DB", "#444A4F", "#262C31", "#E4EAEF", "#4F7799", "#579AD3", "#B7C1CA", "#798590", "#1176DA", "#CBCDCF", "#E2E5E8", "#F9FAFB", "#A7A8A9", "#E4E6E8", "#EDF0F3", "#E2E8EE", "#BCC4CC", "#FAFBFC", "#577696", "#486E96", "#6D7B8A", "#B4C1CF", "#B3BFCC", "#76899E", "#202933", "#1B2026", "#3A5371", "#858A90", "#4B688B", "#8C9BAE", "#6EA2E7", "#808995", "#14325E", "#8D9AAE", "#496CA4", "#A9B3C4", "#344562", "#9EB1D2", "#9DB1D4", "#4B6490", "#344563", "#212732", "#A4B1CA", "#A4B1CA", "#BEBFC1", "#929395", "#20335C", "#8DB0FE", "#3766CF", "#B3CAFE", "#3270FD", "#427BFD", "#343945", "#525B72", "#384568", "#8095DE", "#3F4353", "#1C1F2B", "#606A96", "#4E4F5C", "#373D95", "#8789CC", "#F8F8F9", "#4B4A5C", "#19162A", "#553FA4", "#7156CE", "#221A3C", "#5E4D92", "#3B3747", "#2F2A3D", "#605A6F", "#8F67EB", "#403359", "#A8A6AB", "#1F152D", "#625572", "#6F4B8F", "#50425C", "#4F415A", "#452B58", "#50415A", "#454048", "#493B51", "#714785", "#CDC5D0", "#413E42", "#9A7FA2", "#360D3C", "#988B99", "#7F6D80", "#38133A", "#38133A", "#FFFDFF", "#964C8B", "#CF95C2", "#D8D4D7", "#DACFD7", "#24141F", "#504A4E", "#5A5157", "#C076A7", "#FFD3F0", "#592948", "#5E2347", "#50484C", "#A84271", "#FAA5CC", "#5B283E", "#DF72A0", "#E62878", "#D23577", "#9E5372", "#9C8890", "#EB4D8A", "#C5698C", "#482D37", "#A16C7F", "#B1617D", "#9A3A57", "#D5869D", "#8F777D", "#251D1F", "#D999A6", "#A34558", "#F095A4", "#DB707C", "#C25E69", "#99555B", "#A69A9B", "#B8363E", "#E7262A", "#D36668"]

# RGB Clustering
rgb_colors = [get_rgb(color) for color in colors]
cluster = KMeans(n_clusters=7)
cluster.fit(rgb_colors)
centers = cluster.cluster_centers_
print centers

hex_centers = ['#%02x%02x%02x' % tuple(i) for i in centers]
print hex_centers


# HSV Clustering
"""
hsv_colors = [get_hsv(hex) for hex in colors]
# hsv_colors = [(360 * h, 100 * s, 100 * v) for h, s, v in hsv_colors]
print hsv_colors

cluster = KMeans(n_clusters=7)
cluster.fit(hsv_colors)
centers = cluster.cluster_centers_
print centers
hex_centers = ['#%02x%02x%02x' % colorsys.hsv_to_rgb(i[0], i[1], i[2]) for i in centers]
print json.dumps(hex_centers)
"""