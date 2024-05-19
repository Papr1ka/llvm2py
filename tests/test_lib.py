from llvm2py import parse_assembly
from llvm2py.utils import dump


ir_text = """; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @factorial_req(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, ptr %3, align 4
  %4 = load i32, ptr %3, align 4
  %5 = icmp eq i32 %4, 1
  br i1 %5, label %6, label %7

6:                                                ; preds = %1
  store i32 1, ptr %2, align 4
  br label %13

7:                                                ; preds = %1
  %8 = load i32, ptr %3, align 4
  %9 = sub nsw i32 %8, 1
  %10 = call i32 @factorial_req(i32 noundef %9)
  %11 = load i32, ptr %3, align 4
  %12 = mul nsw i32 %10, %11
  store i32 %12, ptr %2, align 4
  br label %13

13:                                               ; preds = %7, %6
  %14 = load i32, ptr %2, align 4
  ret i32 %14
}"""

dumped_ir = """Function([Argument(0, '%0', Type('i32', <TypeID.IntegerTyID: 13>))], [[], [], ['noundef']], [Block([Instruction(<Opcode.Alloca: 31>, 'alloca', [Value('1', Type('i32', <TypeID.IntegerTyID: 13>))], name='%2', type_=Type('ptr', <TypeID.PointerTyID: 15>)), Instruction(<Opcode.Alloca: 31>, 'alloca', [Value('1', Type('i32', <TypeID.IntegerTyID: 13>))], name='%3', type_=Type('ptr', <TypeID.PointerTyID: 15>)), Instruction(<Opcode.Store: 33>, 'store', [Value('%0', Type('i32', <TypeID.IntegerTyID: 13>)), Value('%3', Type('ptr', <TypeID.PointerTyID: 15>))], name='<badref>', type_=Type('void', <TypeID.VoidTyID: 7>)), Instruction(<Opcode.Load: 32>, 'load', [Value('%3', Type('ptr', <TypeID.PointerTyID: 15>))], name='%4', type_=Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(<Opcode.ICmp: 53>, 'icmp', [Value('%4', Type('i32', <TypeID.IntegerTyID: 13>)), Value('1', Type('i32', <TypeID.IntegerTyID: 13>))], name='%5', type_=Type('i1', <TypeID.IntegerTyID: 13>)), Instruction(<Opcode.Br: 2>, 'br', [Value('%5', Type('i1', <TypeID.IntegerTyID: 13>)), Value('%7', Type('label', <TypeID.LabelTyID: 8>)), Value('%6', Type('label', <TypeID.LabelTyID: 8>))], name='<badref>', type_=Type('void', <TypeID.VoidTyID: 7>))], '%1', [], Type('label', <TypeID.LabelTyID: 8>)), Block([Instruction(<Opcode.Store: 33>, 'store', [Value('1', Type('i32', <TypeID.IntegerTyID: 13>)), Value('%2', Type('ptr', <TypeID.PointerTyID: 15>))], name='<badref>', type_=Type('void', <TypeID.VoidTyID: 7>)), Instruction(<Opcode.Br: 2>, 'br', [Value('%13', Type('label', <TypeID.LabelTyID: 8>))], name='<badref>', type_=Type('void', <TypeID.VoidTyID: 7>))], '%6', ['%1'], Type('label', <TypeID.LabelTyID: 8>)), Block([Instruction(<Opcode.Load: 32>, 'load', [Value('%3', Type('ptr', <TypeID.PointerTyID: 15>))], name='%8', type_=Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(<Opcode.Sub: 15>, 'sub', [Value('%8', Type('i32', <TypeID.IntegerTyID: 13>)), Value('1', Type('i32', <TypeID.IntegerTyID: 13>))], name='%9', type_=Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(<Opcode.Call: 56>, 'call', [Value('%9', Type('i32', <TypeID.IntegerTyID: 13>)), Value('factorial_req', Type('ptr', <TypeID.PointerTyID: 15>))], name='%10', type_=Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(<Opcode.Load: 32>, 'load', [Value('%3', Type('ptr', <TypeID.PointerTyID: 15>))], name='%11', type_=Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(<Opcode.Mul: 17>, 'mul', [Value('%10', Type('i32', <TypeID.IntegerTyID: 13>)), Value('%11', Type('i32', <TypeID.IntegerTyID: 13>))], name='%12', type_=Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(<Opcode.Store: 33>, 'store', [Value('%12', Type('i32', <TypeID.IntegerTyID: 13>)), Value('%2', Type('ptr', <TypeID.PointerTyID: 15>))], name='<badref>', type_=Type('void', <TypeID.VoidTyID: 7>)), Instruction(<Opcode.Br: 2>, 'br', [Value('%13', Type('label', <TypeID.LabelTyID: 8>))], name='<badref>', type_=Type('void', <TypeID.VoidTyID: 7>))], '%7', ['%1'], Type('label', <TypeID.LabelTyID: 8>)), Block([Instruction(<Opcode.Load: 32>, 'load', [Value('%2', Type('ptr', <TypeID.PointerTyID: 15>))], name='%14', type_=Type('i32', <TypeID.IntegerTyID: 13>)), Instruction(<Opcode.Ret: 1>, 'ret', [Value('%14', Type('i32', <TypeID.IntegerTyID: 13>))], name='<badref>', type_=Type('void', <TypeID.VoidTyID: 7>))], '%13', ['%7', '%6'], Type('label', <TypeID.LabelTyID: 8>))], <CallingConv.C: 0>, <LinkageType.ExternalLinkage: 0>, <VisibilityTypes.DefaultVisibility: 0>, Type('i32', <TypeID.IntegerTyID: 13>), 'factorial_req', Type('ptr', <TypeID.PointerTyID: 15>))"""
module = parse_assembly(ir_text)

def test_lib():
    function = module.get_function("factorial_req")
    dumped = dump(function, annotate_fields=False)
    assert dumped_ir == dumped, "Dump is different from the original:\n" + dumped_ir
