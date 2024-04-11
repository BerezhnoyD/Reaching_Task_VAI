M3 = 1.65;
M3F = 1.8;
M3H = 3.1;
LGR = 1.2;

TXB = 10;
TYB = 10;

module top_plate(){
	difference(){
		cube(size=[35,35,3], center=true);

		translate([TXB,TYB,0]) cylinder(r=M3, h=10, center=true);
		translate([-TXB,-TYB,0]) cylinder(r=M3, h=10, center=true);
		translate([TXB,-TYB,0]) cylinder(r=M3, h=10, center=true);
		translate([-TXB,TYB,0]) cylinder(r=M3, h=10, center=true);

		cylinder(r=M3, h=10, center=true);
	}
}

module side(){
	difference(){
		cube(size=[35,4,9], center=true);

		translate([13,0,1.5]) rotate([90,30,0]) cylinder(r=LGR, h=50, $fn=6, center=true);
		translate([-13,0,1.5]) rotate([90,30,0]) cylinder(r=LGR, h=50, $fn=6, center=true);

		translate([0,0,1.5]) rotate([90,30,0]) cylinder(r=M3F, h=50, $fn=12, center=true);
		translate([0,3.5,1.5]) rotate([90,0,0]) cylinder(r=M3H, h=5, $fn=6, center=true);

	}
}

union(){
	top_plate();
	translate([0,4,3.5]) side();
	translate([0,-4,3.5]) rotate([0,0,180]) side();

}