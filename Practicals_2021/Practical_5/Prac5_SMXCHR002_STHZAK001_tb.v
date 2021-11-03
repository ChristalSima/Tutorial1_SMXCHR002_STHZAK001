module ALU8_tb ();

reg clk = 1'b1;
reg [7:0] A = 8'b11110010, B = 8'b00000110;
reg [3:0] ALU_Sel;
wire [7:0] out;
integer i;

ALU8 alu8(.clk(clk), .A(A), .B(B), .ALU_sel(ALU_Sel), .out(out));

initial begin
    $display("For values: A = %b, B %b",A,B);
    $display("ALU_sel   out");
    $monitor("%b      %b",ALU_Sel,out);
    ALU_Sel = 4'b0000;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b0001;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b0010;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b0011;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b0100;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b0101;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b0110;
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b0111;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b1000;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b1001;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b1010;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b1011;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b1100;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b1101;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b1110;
#5
    clk = !clk;
#5
    clk = !clk;
    ALU_Sel = 4'b1111;
#5
    clk = !clk;
#5
    clk = !clk;
end
endmodule