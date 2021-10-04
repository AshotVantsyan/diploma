import matplotlib.pyplot as plt
import numpy as np

def plotTSP(path, points, num_iters=1):

    """
    path: List of lists with the different orders in which the nodes are visited
    points: coordinates for the different nodes
    num_iters: number of paths that are in the path list
    
    """

    # Unpack the primary TSP path and transform it into a list of ordered 
    # coordinates

    x = []; y = []
    for i in paths[0]:
        x.append(points[i][0])
        y.append(points[i][1])
    
    plt.plot(x, y, 'co')

    # Set a scale for the arrow heads (there should be a reasonable default for this, WTF?)
    a_scale = float(100)/float(100)

    # Draw the older paths, if provided
    if num_iters > 1:

        for i in range(1, num_iters):

            # Transform the old paths into a list of coordinates
            xi = []; yi = [];
            for j in paths[i]:
                xi.append(points[j][0])
                yi.append(points[j][1])

            plt.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]), 
                    head_width = a_scale, color = 'r', 
                    length_includes_head = True, ls = 'dashed',
                    width = 0.001/float(num_iters))
            for i in range(0, len(x) - 1):
                plt.arrow(xi[i], yi[i], (xi[i+1] - xi[i]), (yi[i+1] - yi[i]),
                        head_width = a_scale, color = 'r', length_includes_head = True,
                        ls = 'dashed', width = 0.001/float(num_iters))

    # Draw the primary path for the TSP problem
    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width = a_scale, 
            color ='b', length_includes_head=True)
    for i in range(0,len(x)-1):
        plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = a_scale,
                color = 'b', length_includes_head = True)

    #Set axis too slitghtly larger than the set of x and y
    plt.xlim(0, max(x)*1.1)
    plt.ylim(0, max(y)*1.1)
    plt.show()


if __name__ == '__main__':
    # Run an example
    
    # Create a randomn list of coordinates, pack them into a list
    x_cor = np.loadtxt("city_x_coords.csv", delimiter=",")
    y_cor = np.loadtxt("city_y_coords.csv", delimiter=",")
    points = []
    for i in range(0, len(x_cor)):
        points.append((x_cor[i], y_cor[i]))

    # Create two paths, teh second with two values swapped to simulate a 2-OPT
    # Local Search operation
    #path4 = [0, 1, 2, 3, 4, 5, 6]
    #path3 = [0, 2, 1, 3, 4, 5, 6]
    #path2 = [0, 2, 1, 3, 6, 5, 4]
    path1 = [49, 2, 28, 29, 15, 23, 18, 32, 13, 50, 10, 19, 24, 39, 6, 37, 38, 1, 35, 5, 34, 42, 4, 21, 8, 9, 27, 7, 44, 47, 31, 22, 26, 36, 43, 11, 17, 48, 3, 25, 40, 16, 41, 20, 30, 45, 46, 12, 33, 14, 49]
    path1 = [179, 10, 77, 93, 121, 158, 27, 48, 4, 76, 46, 116, 141, 23, 12, 155, 1, 79, 34, 161, 133, 122, 35, 125, 154, 177, 82, 145, 183, 28, 26, 20, 174, 132, 8, 88, 16, 113, 65, 138, 42, 200, 166, 171, 119, 51, 146, 21, 9, 55, 32, 199, 38, 192, 11, 74, 160, 136, 188, 85, 94, 80, 59, 120, 153, 63, 78, 140, 100, 164, 103, 33, 50, 56, 176, 191, 72, 18, 91, 90, 45, 180, 172, 104, 19, 110, 60, 178, 163, 108, 36, 2, 112, 168, 159, 198, 52, 169, 101, 144, 7, 194, 75, 106, 193, 117, 84, 184, 97, 66, 139, 44, 5, 6, 87, 185, 37, 43, 70, 126, 81, 41, 31, 123, 130, 96, 165, 73, 109, 62, 118, 182, 67, 29, 95, 86, 30, 170, 157, 83, 114, 61, 47, 22, 195, 152, 175, 53, 99, 49, 57, 134, 131, 156, 181, 39, 187, 127, 107, 149, 128, 129, 25, 143, 173, 142, 89, 162, 135, 115, 196, 189, 102, 147, 148, 167, 64, 186, 151, 92, 58, 54, 24, 71, 190, 17, 197, 40, 15, 111, 14, 105, 137, 13, 68, 124, 69, 150, 98, 3, 179]
    path1 = [155, 79, 1, 34, 133, 161, 122, 198, 144, 101, 169, 52, 159, 125, 35, 177, 154, 82, 145, 183, 108, 36, 2, 112, 168, 28, 178, 163, 60, 110, 19, 104, 172, 91, 180, 45, 90, 50, 56, 176, 33, 166, 171, 103, 164, 100, 78, 140, 153, 63, 120, 59, 119, 80, 51, 146, 94, 21, 9, 3, 179, 27, 158, 4, 48, 42, 138, 65, 113, 18, 72, 191, 8, 132, 174, 26, 20, 88, 16, 200, 55, 32, 136, 188, 85, 160, 74, 11, 192, 137, 13, 68, 124, 69, 38, 199, 105, 14, 111, 15, 190, 40, 197, 17, 58, 92, 151, 64, 186, 54, 24, 71, 37, 167, 148, 147, 142, 173, 143, 25, 129, 128, 149, 107, 89, 162, 189, 102, 81, 196, 115, 135, 187, 127, 134, 53, 99, 49, 57, 175, 152, 195, 22, 61, 47, 131, 39, 156, 181, 31, 123, 130, 73, 165, 109, 96, 75, 62, 118, 182, 67, 29, 95, 86, 30, 170, 157, 83, 114, 41, 193, 106, 84, 184, 97, 66, 70, 126, 43, 5, 6, 185, 87, 93, 121, 77, 10, 98, 150, 76, 46, 116, 139, 44, 141, 117, 7, 194, 12, 23, 155]
    path1 = [181, 156, 123, 130, 73, 165, 96, 75, 194, 12, 23, 20, 26, 174, 132, 8, 88, 16, 65, 138, 48, 4, 76, 46, 116, 139, 6, 5, 44, 66, 70, 126, 43, 102, 189, 162, 89, 142, 173, 129, 25, 143, 147, 148, 167, 37, 185, 87, 93, 124, 71, 24, 54, 186, 64, 151, 92, 58, 17, 197, 40, 190, 15, 111, 14, 105, 137, 13, 68, 69, 199, 38, 192, 11, 74, 160, 136, 188, 85, 120, 59, 119, 80, 94, 51, 146, 32, 55, 9, 21, 200, 3, 179, 150, 98, 10, 77, 121, 158, 27, 42, 191, 72, 18, 113, 172, 91, 50, 33, 56, 176, 166, 171, 103, 164, 100, 153, 63, 78, 140, 90, 45, 180, 104, 19, 110, 60, 163, 178, 28, 108, 36, 2, 112, 168, 125, 35, 154, 177, 82, 183, 145, 122, 133, 161, 34, 79, 1, 155, 7, 101, 144, 198, 159, 52, 169, 182, 67, 29, 95, 118, 62, 109, 86, 30, 170, 157, 83, 114, 22, 61, 47, 195, 152, 175, 53, 99, 49, 57, 149, 128, 107, 127, 187, 134, 131, 39, 135, 115, 196, 81, 97, 184, 84, 117, 141, 193, 106, 41, 31, 181]
    path1 = [i-1 for i in path1]

    # Pack the paths into a list
    paths = [path1]

    
    # Run the function
    plotTSP(paths, points, 0)