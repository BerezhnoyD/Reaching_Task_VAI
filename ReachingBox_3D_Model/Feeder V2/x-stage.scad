M3 = 1.65;
M3F = 1.8;
M3H = 3.5;
LGR = 1.2;

TYB = 10;
TXB = 10;

module foundation(){
	difference(){
		cube(size=[35,35,3], center=true);

		translate([TXB,TYB,0]) cylinder(r=M3, h=10, center=true);
		translate([-TXB,-TYB,0]) cylinder(r=M3, h=10, center=true);
		translate([TXB,-TYB,0]) cylinder(r=M3, h=10, center=true);
		translate([-TXB,TYB,0]) cylinder(r=M3, h=10, center=true);

		translate([TXB,TYB,1.5]) cylinder(r=M3H, h=3, center=true);
		translate([-TXB,-TYB,1.5]) cylinder(r=M3H, h=3, center=true);
		translate([TXB,-TYB,1.5]) cylinder(r=M3H, h=3, center=true);
		translate([-TXB,TYB,1.5]) cylinder(r=M3H, h=3, center=true);

		cylinder(r=M3, h=10, center=true);
		translate([0,0,1.5]) cylinder(r=3.5, h=3, center=true);

	}
}

module side(){
	difference(){
		cube(size=[35,4,9], center=true);

		translate([13,0,2]) rotate([90,30,0]) cylinder(r=LGR, h=50, $fn=6, center=true);
		translate([-13,0,2]) rotate([90,30,0]) cylinder(r=LGR, h=50, $fn=6, center=true);

		translate([0,0,2]) rotate([90,30,0]) cylinder(r=M3F, h=50, $fn=12, center=true);
	}
}

union(){
	foundation();
	translate([0,15.5,3]) side();
	translate([0,-15.5,3]) side();

}

// +1.5 
// -5.5 + 3 = -2.5
// -2.5 + 11 = 8.5
// -1.5 + 11 = 9.5
//  9.5 - 1.5 = 8
//  9.5 / 2 = 4.75