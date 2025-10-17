Image stylization through triangulated blotching using by Delaunay Triangulation.

Points used to generate the mesh can be distributed via different modes by changing the MODE variable.

The 'uniform' MODE is recommended for most images, this will disperse points evenly throughout the image using an underlying grid,
but allows them to randomly be within a distance to allow for more natural shapes.

![image of uniform stylized lake](https://github.com/Kodiac314/DelaunayTriangulationFilter/blob/main/Images/uniform_wolf2.jpg)

For images with small details that will likely be blurred beyond recognition, the 'dynamic' MODE distribution of points
can be used. It samples points based on the slope of the color gradient, so small contrasting details will likely be included.

![image of dynamic stylized lightning storm](https://github.com/Kodiac314/DelaunayTriangulationFilter/blob/main/Images/dynamic_storm.jpg)

Above, lightning bolts are visibile. Compare this to the 'uniform' MODE distrubution of the same image, where
individual lightning bolts have been blurred away.

![image of uniform stylized lightning storm](https://github.com/Kodiac314/DelaunayTriangulationFilter/blob/main/Images/uniform_storm.jpg)

