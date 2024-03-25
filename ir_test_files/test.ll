; ModuleID = '/app/example.cpp'
source_filename = "/app/example.cpp"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @_Z12do_operationiRfS_(i32 %0, float* nonnull align 4 dereferenceable(4) %1, float* nonnull align 4 dereferenceable(4) %2) #0 !dbg !7 {
  %4 = alloca i32, align 4
  %5 = alloca float*, align 8
  %6 = alloca float*, align 8
  store i32 %0, i32* %4, align 4
  call void @llvm.dbg.declare(metadata i32* %4, metadata !14, metadata !DIExpression()), !dbg !15
  store float* %1, float** %5, align 8
  call void @llvm.dbg.declare(metadata float** %5, metadata !16, metadata !DIExpression()), !dbg !17
  store float* %2, float** %6, align 8
  call void @llvm.dbg.declare(metadata float** %6, metadata !18, metadata !DIExpression()), !dbg !19
  %7 = load i32, i32* %4, align 4, !dbg !20
  %8 = sitofp i32 %7 to float, !dbg !20
  %9 = load float*, float** %5, align 8, !dbg !21
  %10 = load float, float* %9, align 4, !dbg !21
  %11 = load float*, float** %6, align 8, !dbg !22
  %12 = load float, float* %11, align 4, !dbg !22
  %13 = fmul float %10, %12, !dbg !23
  %14 = fadd float %8, %13, !dbg !24
  %15 = fptosi float %14 to i32, !dbg !20
  ret i32 %15, !dbg !25
}

; Function Attrs: nounwind readnone speculatable willreturn
declare void @llvm.dbg.declare(metadata, metadata, metadata) #1

; Function Attrs: noinline norecurse nounwind optnone uwtable
define dso_local i32 @main() #2 !dbg !26 {
  %1 = alloca i32, align 4
  %2 = alloca float, align 4
  %3 = alloca float, align 4
  %4 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  call void @llvm.dbg.declare(metadata float* %2, metadata !29, metadata !DIExpression()), !dbg !30
  store float 5.000000e+00, float* %2, align 4, !dbg !30
  call void @llvm.dbg.declare(metadata float* %3, metadata !31, metadata !DIExpression()), !dbg !32
  store float 5.000000e+00, float* %3, align 4, !dbg !32
  call void @llvm.dbg.declare(metadata i32* %4, metadata !33, metadata !DIExpression()), !dbg !34
  %5 = call i32 @_Z12do_operationiRfS_(i32 5, float* nonnull align 4 dereferenceable(4) %2, float* nonnull align 4 dereferenceable(4) %3), !dbg !35
  store i32 %5, i32* %4, align 4, !dbg !34
  ret i32 0, !dbg !36
}

attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable willreturn }
attributes #2 = { noinline norecurse nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.dbg.cu = !{!0}
!llvm.module.flags = !{!3, !4, !5}
!llvm.ident = !{!6}

!0 = distinct !DICompileUnit(language: DW_LANG_C_plus_plus_14, file: !1, producer: "clang version 11.0.0 (https://github.com/llvm/llvm-project.git 176249bd6732a8044d457092ed932768724a6f06)", isOptimized: false, runtimeVersion: 0, emissionKind: FullDebug, enums: !2, splitDebugInlining: false, nameTableKind: None)
!1 = !DIFile(filename: "/app/example.cpp", directory: "/app")
!2 = !{}
!3 = !{i32 7, !"Dwarf Version", i32 4}
!4 = !{i32 2, !"Debug Info Version", i32 3}
!5 = !{i32 1, !"wchar_size", i32 4}
!6 = !{!"clang version 11.0.0 (https://github.com/llvm/llvm-project.git 176249bd6732a8044d457092ed932768724a6f06)"}
!7 = distinct !DISubprogram(name: "do_operation", linkageName: "_Z12do_operationiRfS_", scope: !8, file: !8, line: 2, type: !9, scopeLine: 3, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !2)
!8 = !DIFile(filename: "example.cpp", directory: "/app")
!9 = !DISubroutineType(types: !10)
!10 = !{!11, !11, !12, !12}
!11 = !DIBasicType(name: "int", size: 32, encoding: DW_ATE_signed)
!12 = !DIDerivedType(tag: DW_TAG_reference_type, baseType: !13, size: 64)
!13 = !DIBasicType(name: "float", size: 32, encoding: DW_ATE_float)
!14 = !DILocalVariable(name: "a", arg: 1, scope: !7, file: !8, line: 2, type: !11)
!15 = !DILocation(line: 2, column: 22, scope: !7)
!16 = !DILocalVariable(name: "b", arg: 2, scope: !7, file: !8, line: 2, type: !12)
!17 = !DILocation(line: 2, column: 32, scope: !7)
!18 = !DILocalVariable(name: "c", arg: 3, scope: !7, file: !8, line: 2, type: !12)
!19 = !DILocation(line: 2, column: 42, scope: !7)
!20 = !DILocation(line: 4, column: 12, scope: !7)
!21 = !DILocation(line: 4, column: 16, scope: !7)
!22 = !DILocation(line: 4, column: 20, scope: !7)
!23 = !DILocation(line: 4, column: 18, scope: !7)
!24 = !DILocation(line: 4, column: 14, scope: !7)
!25 = !DILocation(line: 4, column: 5, scope: !7)
!26 = distinct !DISubprogram(name: "main", scope: !8, file: !8, line: 7, type: !27, scopeLine: 8, flags: DIFlagPrototyped, spFlags: DISPFlagDefinition, unit: !0, retainedNodes: !2)
!27 = !DISubroutineType(types: !28)
!28 = !{!11}
!29 = !DILocalVariable(name: "b", scope: !26, file: !8, line: 9, type: !13)
!30 = !DILocation(line: 9, column: 11, scope: !26)
!31 = !DILocalVariable(name: "d", scope: !26, file: !8, line: 10, type: !13)
!32 = !DILocation(line: 10, column: 11, scope: !26)
!33 = !DILocalVariable(name: "i", scope: !26, file: !8, line: 11, type: !11)
!34 = !DILocation(line: 11, column: 9, scope: !26)
!35 = !DILocation(line: 11, column: 13, scope: !26)
!36 = !DILocation(line: 12, column: 5, scope: !26)
