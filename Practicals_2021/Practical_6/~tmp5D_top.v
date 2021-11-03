`timescale 1ns / 1ps

module simple_cpu( clk, rst, instruction );

    parameter DATA_WIDTH = 8; //8 bit wide data
    parameter ADDR_BITS = 5; //32 Addresses
    parameter INSTR_WIDTH = 20; //20b instruction

    input [INSTR_WIDTH-1:0] instruction;
    input clk, rst;

    //Wires for connecting to data memory    
    wire [ADDR_BITS-1:0] addr_i;
    wire [DATA_WIDTH-1:0] data_in_i, data_out_i, result2_i ;
    wire wen_i; 
    
    //wire for connecting to the ALU
    wire [DATA_WIDTH-1:0] operand_a_i, operand_b_i, result1_i;
    wire [3:0] opcode_i;
    
   
    //Wire for connecting to CU
    wire [DATA_WIDTH-1:0]offset_i;
    wire sel1_i, sel3_i;
    wire [DATA_WIDTH-1:0] operand_1_i, operand_2_i;
    //Output Register (packed) for CU internal register
  	reg [4*DATA_WIDTH-1:0] Reg_file;
    //Top.v unpacking vectors for assignment with output from Reg_file
    reg [DATA_WIDTH-1:0] CU_regfile_0;
    reg [DATA_WIDTH-1:0] CU_regfile_1;
    reg [DATA_WIDTH-1:0] CU_regfile_2;
    reg [DATA_WIDTH-1:0] CU_regfile_3;
    
    //Instantiating an alu1
    alu #(DATA_WIDTH) alu1 (clk, operand_a_i, operand_b_i, opcode_i, result1_i);
     
    //instantiation of data memory
    reg_mem  #(DATA_WIDTH,ADDR_BITS) data_memory(result1_i, data_in_i, wen_i, clk, data_out_i);
    
    //Instantiation of a CU
    CU  #(DATA_WIDTH,ADDR_BITS, INSTR_WIDTH) CU1(clk, rst, instruction, result2_i,
        operand_1_i, operand_2_i, offset_i, opcode_i, sel1_i, sel3_i, wen_i, Reg_file);
    
    //Connect CU to ALU
    assign operand_a_i = operand_1_i;
    assign operand_b_i = (sel3_i == 0) ? operand_2_i: (sel3_i == 1) ? offset_i : 8'bx;
    
    //Connect CU to Memory
    assign data_in_i = operand_2_i;
    
    //Connect datamem to CU
    assign result2_i = (sel1_i == 0) ? data_out_i : (sel1_i == 1) ? result1_i : 8'bx;  
    
    //Assigning outputs from packed Reg_file register into top.v registers
  	assign CU_regfile_0 = Reg_file[7:0];
  	assign CU_regfile_1 = Reg_file[15:8];
  	assign CU_regfile_2 = Reg_file[23:16];
  	assign CU_regfile_3 = Reg_file[31:24];
    
    
    
    
















endmodule


















