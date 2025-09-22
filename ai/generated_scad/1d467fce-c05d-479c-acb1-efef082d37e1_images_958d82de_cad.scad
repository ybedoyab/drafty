$fn = 100;

length = 500;
width = 300;
height = 150;

module main() {
  linear_extrude(height=width, center=false) {
    polygon(points=[[0,0], [length,0], [0,height]]);
  }
}

main();