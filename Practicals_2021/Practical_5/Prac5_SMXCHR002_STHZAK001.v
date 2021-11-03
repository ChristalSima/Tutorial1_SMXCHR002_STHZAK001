module ALU8(
    input clk,
    input [7:0] A, B,
    input [3:0] ALU_sel,
    output reg [7:0] out
);

 reg [7:0] Acc;
 integer hold;

 always @ (posedge clk) begin
    case (ALU_sel)
        /*ADD*/  4'b0000 : Acc = A + B;
        /*SUB*/  4'b0001 : Acc = A - B;
        /*MUL*/  4'b0010 : Acc = A*B;
        /*DIV*/  4'b0011 : Acc = A/B;

        /*ADDA*/ 4'b0100 : Acc = Acc + A;
        /*MULA*/ 4'b0101 : Acc = Acc*A;
        /*MAC*/  4'b0110 : Acc = Acc + (A*B);

        /*ROL*/  4'b0111 : begin
            hold = A[7];
            Acc = A << 1; //Logical shift left pads with zero
            Acc[0] = hold;
        end

        /*ROR*/  4'b1000 : begin
            hold = A[0];
            Acc = A >> 1; //Logical shift right pads with zero
            Acc[7] = hold;
        end

        /*AND*/  4'b1001 : Acc = A & B; //Bitwise AND
        /*OR*/   4'b1010 : Acc = A | B; //Bitwise OR
        /*XOR*/  4'b1011 : Acc = A ^ B; //Bitwise XOR
        /*NAND*/ 4'b1100 : Acc = ~ (A & B); //Bitwise "NOT AND" NAND

        /*ETH*/  4'b1101 : if (A == B) Acc = 8'hFF;
            else Acc = 8'h0;
        
        /*GTH*/  4'b1110 : if (A > B) Acc = 8'hFF;
            else Acc = 8'h0;

        /*LTH*/  4'b1111 : if (A < B) Acc = 8'hFF;
            else Acc = 8'h0;

    endcase
    out = Acc;
 end
endmodule