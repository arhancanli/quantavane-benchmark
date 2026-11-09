#!/bin/sh
# Expected verdicts on the reference submissions: "page" then "verified in review".
cd "$(dirname "$0")"
status=0
t() {  # t PROBLEM FILE EXPECTED
  got=$(python3 -I obb.py check "$1" "$2" | grep -o 'IMPROVES\|does not improve\|NOT CERTIFIED' | tr '\n' ',')
  if [ "$got" = "$3" ]; then echo "ok    $1 $(basename $2): $got"; else echo "FAIL  $1 $(basename $2): $got (expected $3)"; status=1; fi
}
echo '{"values": [1, 1, 1, 1]}' > certs/flat4_1a.json
t 1a-upper certs/flat4_1a.json "does not improve,does not improve,does not improve,"
t 1c-lower certs/kos_1c.json "does not improve,does not improve,"
t 1c-lower certs/vid_1c_v3.json "IMPROVES,does not improve,"
t 1d-upper certs/huiihao_1d.json "does not improve,does not improve,"
t 68a-lower certs/pin_68a.json "does not improve,does not improve,"
t 68a-lower certs/vid_68a_044605.json "IMPROVES,does not improve,"
t ramsey-6-8 certs/cremer_6_8_n134.txt "does not improve,"
t sphere-d3-n952 refs/ours_sphere_d3_n952.txt "does not improve,"
t sphere-d4-n310 refs/ours_sphere_d4_n310.txt "does not improve,"
t sphere-d5-n267 refs/ours_sphere_d5_n267.txt "does not improve,"
t sphere-d6-n188 refs/ours_sphere_d6_n188.txt "does not improve,"
t sphere-d8-n119 refs/ours_sphere_d8_n119.txt "does not improve,"
t sphere-d10-n176 refs/ours_sphere_d10_n176.txt "does not improve,"
t sphere-d12-n103 refs/ours_sphere_d12_n103.txt "does not improve,"
t sphere-d16-n63 refs/ours_sphere_d16_n63.txt "does not improve,"
t sphere-d20-n86 refs/ours_sphere_d20_n86.txt "does not improve,"
t sphere-d24-n71 refs/ours_sphere_d24_n71.txt "does not improve,"
t sphere-d32-n84 refs/ours_sphere_d32_n84.txt "does not improve,"
t covering-36-6-2 refs/ours_covering_36-6-2.txt "does not improve,"
t covering-35-10-3 refs/ours_covering_35-10-3.txt "does not improve,"
t covering-28-17-4 refs/ours_covering_28-17-4.txt "does not improve,"
t covering-22-15-6 refs/ours_covering_22-15-6.txt "does not improve,"
t covering-24-17-7 refs/ours_covering_24-17-7.txt "does not improve,"
t covering-37-8-2-3 refs/ours_covering_37-8-2-3.txt "does not improve,"
t covering-21-8-3-4 refs/ours_covering_21-8-3-4.txt "does not improve,"
t covering-17-7-4-6 refs/ours_covering_17-7-4-6.txt "does not improve,"
t covering-18-9-5-6 refs/ours_covering_18-9-5-6.txt "does not improve,"
t covering-23-6-6-15 refs/ours_covering_23-6-6-15.txt "does not improve,"
t 42a-upper certs/griego_c42.json "does not improve,"
t 42a-upper certs/pinho_c42_256.json "does not improve,"
t 59a-upper certs/gomyway_c59.json "IMPROVES,does not improve,"
t 16a-lower refs/maxr_c16_lower.json "does not improve,does not improve,"
t 16a-lower refs/vid_c16_lower.json "IMPROVES,does not improve,"
t cvrp-antwerp1 refs/ours_cvrp_Antwerp1.sol "does not improve,"
t cvrp-antwerp2 refs/ours_cvrp_Antwerp2.sol "does not improve,"
t cvrp-brussels1 refs/ours_cvrp_Brussels1.sol "does not improve,"
t cvrp-brussels2 refs/ours_cvrp_Brussels2.sol "does not improve,"
t cvrp-flanders1 refs/ours_cvrp_Flanders1.sol "does not improve,"
t cvrp-flanders2 refs/ours_cvrp_Flanders2.sol "does not improve,"
t cvrp-ghent1 refs/ours_cvrp_Ghent1.sol "does not improve,"
t cvrp-ghent2 refs/ours_cvrp_Ghent2.sol "does not improve,"
t cvrp-leuven2 refs/ours_cvrp_Leuven2.sol "does not improve,"
t cvrp-xl-n1048-k237 refs/ours_cvrp_XL-n1048-k237.sol "does not improve,"
t cvrp-xl-n1748-k271 refs/ours_cvrp_XL-n1748-k271.sol "does not improve,"
t cvrp-xl-n6168-k1922 refs/ours_cvrp_XL-n6168-k1922.sol "does not improve,"
t cvrp-xl-n8028-k294 refs/ours_cvrp_XL-n8028-k294.sol "does not improve,"
t cvrp-xl-n9784-k2774 refs/ours_cvrp_XL-n9784-k2774.sol "does not improve,"
# controls: a solution with a route removed, and one with two routes joined (load 256 > capacity 128)
sed '1d' refs/ours_cvrp_XL-n1048-k237.sol > certs/control_cvrp_missing_route.sol
t cvrp-xl-n1048-k237 certs/control_cvrp_missing_route.sol "NOT CERTIFIED,"
sed '1{N;s/\nRoute #[0-9]*://;}' refs/ours_cvrp_XL-n1048-k237.sol > certs/control_cvrp_overfull.sol
t cvrp-xl-n1048-k237 certs/control_cvrp_overfull.sol "NOT CERTIFIED,"
t cw-27-4-6 refs/ours_cw_27_4_6.txt "does not improve,"
t cw-28-4-5 refs/ours_cw_28_4_5.txt "does not improve,"
t cw-29-4-5 refs/ours_cw_29_4_5.txt "does not improve,"
t cw-33-4-5 refs/ours_cw_33_4_5.txt "does not improve,"
t cw-33-6-6 refs/ours_cw_33_6_6.txt "does not improve,"
t cw-34-6-5 refs/ours_cw_34_6_5.txt "does not improve,"
t cw-34-6-6 refs/ours_cw_34_6_6.txt "does not improve,"
t cw-35-6-5 refs/ours_cw_35_6_5.txt "does not improve,"
t cw-35-6-6 refs/ours_cw_35_6_6.txt "does not improve,"
t cw-36-4-5 refs/ours_cw_36_4_5.txt "does not improve,"
t cw-36-6-5 refs/ours_cw_36_6_5.txt "does not improve,"
t cw-38-4-5 refs/ours_cw_38_4_5.txt "does not improve,"
t cw-38-6-6 refs/ours_cw_38_6_6.txt "does not improve,"
t cw-39-4-5 refs/ours_cw_39_4_5.txt "does not improve,"
t cw-40-4-5 refs/ours_cw_40_4_5.txt "does not improve,"
t cw-40-6-5 refs/ours_cw_40_6_5.txt "does not improve,"
t cw-42-6-5 refs/ours_cw_42_6_5.txt "does not improve,"
t cw-42-6-6 refs/ours_cw_42_6_6.txt "does not improve,"
t cw-44-6-5 refs/ours_cw_44_6_5.txt "does not improve,"
t cw-45-6-5 refs/ours_cw_45_6_5.txt "does not improve,"
t cw-46-6-5 refs/ours_cw_46_6_5.txt "does not improve,"
t cw-47-6-5 refs/ours_cw_47_6_5.txt "does not improve,"
t cw-50-6-5 refs/ours_cw_50_6_5.txt "does not improve,"
t cw-51-6-5 refs/ours_cw_51_6_5.txt "does not improve,"
t cw-51-6-6 refs/ours_cw_51_6_6.txt "does not improve,"
t cw-52-6-5 refs/ours_cw_52_6_5.txt "does not improve,"
t cw-53-6-5 refs/ours_cw_53_6_5.txt "does not improve,"
t cw-54-6-5 refs/ours_cw_54_6_5.txt "does not improve,"
t cw-55-6-5 refs/ours_cw_55_6_5.txt "does not improve,"
t cw-56-6-5 refs/ours_cw_56_6_5.txt "does not improve,"
t cw-58-6-5 refs/ours_cw_58_6_5.txt "does not improve,"
t cw-60-6-5 refs/ours_cw_60_6_5.txt "does not improve,"
# controls: a code with its first word repeated, and one with a word of the wrong weight
sed -n '1p' refs/ours_cw_34_6_5.txt | cat - refs/ours_cw_34_6_5.txt > certs/control_cw_repeated.txt
t cw-34-6-5 certs/control_cw_repeated.txt "NOT CERTIFIED,"
sed '1s/$/ 34/' refs/ours_cw_34_6_5.txt > certs/control_cw_weight.txt
t cw-34-6-5 certs/control_cw_weight.txt "NOT CERTIFIED,"
# v1.1: our public Ramsey colourings (arhancanli/quantavane-ramsey-records), our cage graphs sent to House of Graphs,
# and classical constructions built by our own code (refs/README.md)
t ramsey-3-18 refs/ours_ramsey_3_18_n100.txt "does not improve,"
t ramsey-4-18 refs/ours_ramsey_4_18_n210.txt "does not improve,"
t ramsey-5-15 refs/ours_ramsey_5_15_n282.txt "does not improve,"
t cage-6-9 refs/ours_cage_6_9_n5600.s6 "IMPROVES,does not improve,"
t cage-7-9 refs/ours_cage_7_9_n17600.s6 "IMPROVES,does not improve,"
t multiramsey-3-3-3-3 refs/classic_multiramsey_3333_n32.txt "does not improve,"
t multiramsey-4-4-4 refs/classic_multiramsey_444_n127.txt "does not improve,"
t kissing-d5 refs/classic_kissing_d5_D5_n40.txt "does not improve,"
t kissing-d6 refs/classic_kissing_d6_E6_n72.txt "does not improve,"
t kissing-d7 refs/classic_kissing_d7_E7_n126.txt "does not improve,"
t kissing-d16 refs/classic_kissing_d16_BW16_n4320.txt "does not improve,"
t sortnet-n13-size refs/classic_sortnet_batcher_n13.txt "does not improve,"
t sortnet-n16-size refs/classic_sortnet_batcher_n16.txt "does not improve,"
t sortnet-n20-size refs/classic_sortnet_batcher_n20.txt "does not improve,"
t sortnet-n24-size refs/classic_sortnet_batcher_n24.txt "does not improve,"
t sortnet-n28-size refs/classic_sortnet_batcher_n28.txt "does not improve,"
t sortnet-n32-size refs/classic_sortnet_batcher_n32.txt "does not improve,"
t sortnet-n33-size refs/classic_sortnet_batcher_n33.txt "does not improve,"
t golomb-29 refs/classic_golomb_erdos_turan_m29.txt "does not improve,"
t golomb-30 refs/classic_golomb_erdos_turan_m30.txt "does not improve,"
t superperm-n8 refs/classic_superperm_n8.txt "does not improve,"
t superperm-n9 refs/classic_superperm_n9.txt "does not improve,"
t shannon-c7-power5 refs/classic_shannon_c7_k5_n243.txt "does not improve,"
# v1.1: Leaps in Bounds certificates (fetch.sh), replayed by our checkers
t snake-d9 certs/lib_snake-in-the-box-9-lower-191.txt "does not improve,"
t snake-d10 certs/lib_snake-in-the-box-10-lower-379.txt "does not improve,"
t snake-d11 certs/lib_snake-in-the-box-11-lower-750.txt "does not improve,"
t snake-d12 certs/lib_snake-in-the-box-12-lower-1480.txt "does not improve,"
t snake-d13 certs/lib_snake-in-the-box-13-lower-2946.txt "does not improve,"
t coil-d9 certs/lib_coil-in-the-box-9-lower-192.txt "does not improve,"
t coil-d10 certs/lib_coil-in-the-box-10-lower-374.txt "does not improve,"
t coil-d11 certs/lib_coil-in-the-box-11-lower-740.txt "does not improve,"
t coil-d12 certs/lib_coil-in-the-box-12-lower-1468.txt "does not improve,"
t coil-d13 certs/lib_coil-in-the-box-13-lower-2930.txt "does not improve,"
t capset-n7 certs/lib_cap-set-7-lower-236.txt "does not improve,"
t capset-n8 certs/lib_cap-set-8-lower-512.txt "does not improve,"
t superperm-n6 certs/lib_minimal-superpermutation-6-upper-873.txt "does not improve,"
t superperm-n7 certs/lib_minimal-superpermutation-7-upper-5913.txt "does not improve,"
t schur-6 certs/lib_schur-6-lower-537.txt "does not improve,"
t schur-7 certs/lib_schur-7-lower-1696.txt "does not improve,"
t schur-8 certs/lib_schur-8-lower-5372.txt "does not improve,"
t weak-schur-5 certs/lib_weak-schur-5-lower-207.txt "does not improve,"
t weak-schur-6 certs/lib_weak-schur-6-lower-650.txt "does not improve,"
t vdw-2-7 certs/lib_van-der-waerden-2-7-lower-3704.txt "does not improve,"
t vdw-2-8 certs/lib_van-der-waerden-2-8-lower-11496.txt "does not improve,"
t vdw-4-4 certs/lib_van-der-waerden-4-4-lower-1049.txt "does not improve,"
t vdw-4-5 certs/lib_van-der-waerden-4-5-lower-17706.txt "does not improve,"
t vdw-5-4 certs/lib_van-der-waerden-5-4-lower-2255.txt "does not improve,"
t vdw-6-4 certs/lib_van-der-waerden-6-4-lower-9779.txt "does not improve,"
t no3line-75 certs/lib_no-three-in-line-75-lower-148.txt "does not improve,"
t no3line-77 certs/lib_no-three-in-line-77-lower-152.txt "does not improve,"
t degdiam-3-5 certs/lib_degree-diameter-3-5-lower-64.s6 "does not improve,"
t degdiam-3-6 certs/lib_degree-diameter-3-6-lower-64.s6 "does not improve,"
t degdiam-3-7 certs/lib_degree-diameter-3-7-lower-162.s6 "does not improve,"
t degdiam-3-8 certs/lib_degree-diameter-3-8-lower-272.s6 "does not improve,"
t degdiam-3-9 certs/lib_degree-diameter-3-9-lower-506.s6 "does not improve,"
t degdiam-3-10 certs/lib_degree-diameter-3-10-lower-820.s6 "does not improve,"
t degdiam-4-3 certs/lib_degree-diameter-4-3-lower-41.s6 "does not improve,"
t degdiam-4-4 certs/lib_degree-diameter-4-4-lower-84.s6 "does not improve,"
t degdiam-4-5 certs/lib_degree-diameter-4-5-lower-205.s6 "does not improve,"
t degdiam-5-3 certs/lib_degree-diameter-5-3-lower-54.s6 "does not improve,"
t degdiam-5-4 certs/lib_degree-diameter-5-4-lower-210.s6 "does not improve,"
t degdiam-8-2 certs/lib_degree-diameter-8-2-lower-57.s6 "does not improve,"
t degdiam-8-3 certs/lib_degree-diameter-8-3-lower-253.s6 "does not improve,"
t degdiam-8-4 certs/lib_degree-diameter-8-4-lower-1029.s6 "does not improve,"
t degdiam-9-3 certs/lib_degree-diameter-9-3-lower-256.s6 "does not improve,"
t degdiam-10-2 certs/lib_degree-diameter-10-2-lower-91.s6 "does not improve,"
t degdiam-10-3 certs/lib_degree-diameter-10-3-lower-366.s6 "does not improve,"
t degdiam-11-3 certs/lib_degree-diameter-11-3-lower-420.s6 "does not improve,"
# the Schur partitions of 1..537 and 1..1696 colour K_538 and K_1697 without monochromatic triangles (edge {i,j} by
# the class of |i-j|): R_6(3) >= 539 and R_7(3) >= 1698
schur_to_kn() { python3 -I -c 'import sys
s = "".join(open(sys.argv[1]).read().split())
n = len(s) + 1
sys.stdout.write("".join("".join("-" if i == j else s[abs(i - j) - 1] for j in range(n)) + "\n" for i in range(n)))' "$1"; }
schur_to_kn certs/lib_schur-6-lower-537.txt > certs/derived_r63_from_schur6_n538.txt
t multiramsey-3-3-3-3-3-3 certs/derived_r63_from_schur6_n538.txt "does not improve,"
schur_to_kn certs/lib_schur-7-lower-1696.txt > certs/derived_r73_from_schur7_n1697.txt
t multiramsey-3-3-3-3-3-3-3 certs/derived_r73_from_schur7_n1697.txt "does not improve,"
# v1.1 red controls: each must be refused
cp refs/ours_ramsey_3_18_n100.txt certs/control_ramsey_blue_k17.txt            # independence number 17: a blue K_17
t ramsey-3-17 certs/control_ramsey_blue_k17.txt "NOT CERTIFIED,"
printf -- '-00\n0-0\n00-\n' > certs/control_multiramsey_triangle.txt            # a triangle in colour 0
t multiramsey-3-3-3-3 certs/control_multiramsey_triangle.txt "NOT CERTIFIED,"
printf '0 1\n1 2\n2 3\n3 4\n4 0\n0 5\n1 6\n2 7\n3 8\n4 9\n5 7\n7 9\n9 6\n6 8\n8 5\n' > certs/control_cage_petersen.txt
t cage-3-13 certs/control_cage_petersen.txt "NOT CERTIFIED,"                    # cubic, girth 5
sed '$d' certs/control_cage_petersen.txt > certs/control_cage_not_regular.txt
t cage-3-13 certs/control_cage_not_regular.txt "NOT CERTIFIED,"                 # two vertices of degree 2
cp refs/ours_cage_6_9_n5600.s6 certs/control_cage_girth9_as_10.s6
t cage-6-10 certs/control_cage_girth9_as_10.s6 "NOT CERTIFIED,"                 # girth 9, not 10
printf '0 1\n0 2\n0 3\n0 4\n' > certs/control_degdiam_star.txt
t degdiam-3-5 certs/control_degdiam_star.txt "NOT CERTIFIED,"                   # degree 4 > 3
cp certs/lib_degree-diameter-3-10-lower-820.s6 certs/control_degdiam_diameter10_as_9.s6
t degdiam-3-9 certs/control_degdiam_diameter10_as_9.s6 "NOT CERTIFIED,"         # diameter 10 > 9
(grep -v '^#' refs/classic_kissing_d5_D5_n40.txt | head -1; cat refs/classic_kissing_d5_D5_n40.txt) > certs/control_kissing_repeat.txt
t kissing-d5 certs/control_kissing_repeat.txt "NOT CERTIFIED,"                  # a vector twice
cp refs/classic_kissing_d6_E6_n72.txt certs/control_kissing_rank6_as_5.txt
t kissing-d5 certs/control_kissing_rank6_as_5.txt "NOT CERTIFIED,"              # spans dimension 6
(cat refs/classic_kissing_d5_D5_n40.txt; echo '2 0 0 0 0') > certs/control_kissing_norm.txt
t kissing-d5 certs/control_kissing_norm.txt "NOT CERTIFIED,"                    # squared norm 4, not 2
sed '$d' refs/classic_sortnet_batcher_n16.txt > certs/control_sortnet_missing_last.txt
t sortnet-n16-size certs/control_sortnet_missing_last.txt "NOT CERTIFIED,"     # last comparator removed
printf '0000000\n' > certs/control_vdw_ap.txt
t vdw-2-7 certs/control_vdw_ap.txt "NOT CERTIFIED,"                             # 1..7 in one colour
printf '000\n' > certs/control_schur_sum.txt
t schur-6 certs/control_schur_sum.txt "NOT CERTIFIED,"                          # 1 + 1 = 2
printf '0000\n' > certs/control_weak_schur_sum.txt
t weak-schur-5 certs/control_weak_schur_sum.txt "NOT CERTIFIED,"                # 1 + 2 = 3
printf '00\n' > certs/control_snake_back.txt
t snake-d9 certs/control_snake_back.txt "NOT CERTIFIED,"                        # returns to the vertex 0
cp certs/lib_snake-in-the-box-9-lower-191.txt certs/control_coil_open.txt
t coil-d9 certs/control_coil_open.txt "NOT CERTIFIED,"                          # a snake does not close
printf '0000000 1111111 2222222\n' > certs/control_capset_line.txt
t capset-n7 certs/control_capset_line.txt "NOT CERTIFIED,"                      # three points on a line
printf '123456\n' > certs/control_superperm_short.txt
t superperm-n6 certs/control_superperm_short.txt "NOT CERTIFIED,"
seq 0 28 > certs/control_golomb_repeat.txt
t golomb-29 certs/control_golomb_repeat.txt "NOT CERTIFIED,"                    # difference 1 repeated
printf '0,0 1,1 2,2\n' > certs/control_no3line_diagonal.txt
t no3line-75 certs/control_no3line_diagonal.txt "NOT CERTIFIED,"
python3 -I -c 'print(("+" * 668 + "\n") * 668, end="")' > certs/control_hadamard_all_plus.txt
t hadamard-668 certs/control_hadamard_all_plus.txt "NOT CERTIFIED,"
python3 -I -c 'H = [[1]]
for _ in range(4):
    H = [r + r for r in H] + [r + [-x for x in r] for r in H]
print("\n".join("".join("+" if x > 0 else "-" for x in r) for r in H))' > certs/unit_sylvester16.txt
t hadamard-668 certs/unit_sylvester16.txt "NOT CERTIFIED,"                      # a Hadamard matrix of the wrong order
python3 -I -c 'print(" ".join(["0"] * 155))' > certs/control_cwm_zero.txt
t cwm-155-25 certs/control_cwm_zero.txt "NOT CERTIFIED,"                        # weight 0, not 25
printf '00000\n00001\n' > certs/control_strongpow_adjacent.txt
t shannon-c7-power5 certs/control_strongpow_adjacent.txt "NOT CERTIFIED,"
# v2.1, Prestige 100: record certificates fetched by fetch.sh, replayed by our checkers (each equals its record)
t tsp-mona-lisa certs/cook_monalisa_5757191.tour "does not improve,"            # Nagata's tour, 5,757,191
t matmul-3x3x3 certs/fmm_3x3x3_23.json "does not improve,"                      # Laderman's 23 (catalogue, l = 1)
t matmul-4x4x4 certs/fmm_4x4x4_48.json "does not improve,"                      # the catalogue's 48, rational coefficients
t schur-6 certs/derived_mckenna_schur6_538.txt "does not improve,"              # McKenna's S(6) >= 538
t weak-schur-7 certs/lib_weak-schur-7-lower-2154.txt "does not improve,"        # ours, merged by Leaps in Bounds
t weak-schur-8 certs/lib_weak-schur-8-lower-7002.txt "does not improve,"
t weak-schur-9 certs/lib_weak-schur-9-lower-22620.txt "does not improve,"
t ramsey-6-6 certs/derived_lib_ramsey-6-6-lower-102.txt "does not improve,"     # Kalbfleisch's K_101
t ramsey-7-7 certs/derived_lib_ramsey-7-7-lower-205.txt "does not improve,"     # Mathon's K_204
t ramsey-8-8 certs/derived_lib_ramsey-8-8-lower-282.txt "does not improve,"     # Burling and Reyner's K_281
t sortnet-n13-size certs/dobb_n13_s45.txt "does not improve,"                   # B. Dobbelaere's list
t sortnet-n14-size certs/dobb_n14_s51.txt "does not improve,"
t sortnet-n15-size certs/dobb_n15_s56.txt "does not improve,"
t sortnet-n16-size certs/dobb_n16_s60.txt "does not improve,"                   # Green's 60 (1969)
t sortnet-n17-size certs/dobb_n17_s71.txt "does not improve,"
t 1a-upper certs/ours_c1a_upper_n262144.json "IMPROVES,does not improve,IMPROVES,"  # ours, pull request #346 in review
dn() { python3 -I -c 'import itertools, sys
n = int(sys.argv[1])
for i, j in itertools.combinations(range(n), 2):
    for a in (1, -1):
        for b in (1, -1):
            v = [0] * n; v[i], v[j] = a, b; print(" ".join(map(str, v)))' "$1"; }
dn 22 > certs/classic_kissing_D22.txt
t kissing-d22 certs/classic_kissing_D22.txt "does not improve,"                 # the 924 roots of D22
dn 31 > certs/classic_kissing_D31.txt
t kissing-d31 certs/classic_kissing_D31.txt "does not improve,"                 # the 1,860 roots of D31
dn 23 > certs/control_kissing_D23_as_22.txt
t kissing-d22 certs/control_kissing_D23_as_22.txt "NOT CERTIFIED,"              # spans dimension 23
# v2.1 red controls on the new problems: each must be refused
seq 1 32 > certs/control_costas_identity.txt
t costas-32 certs/control_costas_identity.txt "NOT CERTIFIED,"                  # every shift-1 difference is 1
t moore-57 certs/control_cage_petersen.txt "NOT CERTIFIED,"                     # the Moore graph of degree 3, not 57
t srg-99-14-1-2 certs/control_cage_petersen.txt "NOT CERTIFIED,"
t srg-88-27-6-9 certs/control_cage_petersen.txt "NOT CERTIFIED,"
python3 -I -c 'print("\n".join(" ".join(str((i + j) % 10) for j in range(10)) for i in range(10)))' > certs/control_mols_cyclic.txt
cat certs/control_mols_cyclic.txt certs/control_mols_cyclic.txt > certs/control_mols_equal.txt
t mols-10 certs/control_mols_equal.txt "NOT CERTIFIED,"                         # a square is not orthogonal to itself
python3 -I -c 'print("\n".join(" ".join(str(x) for x in range(13 * r, 13 * r + 13)) for r in range(12)))' > certs/control_projplane_disjoint.txt
t projplane-12 certs/control_projplane_disjoint.txt "NOT CERTIFIED,"            # 12 disjoint lines, not a plane
python3 -I -c 'import json, sys
d = json.load(open(sys.argv[1])); t = d["terms"][0][0]
r, c = next((r, c) for r in range(3) for c in range(3) if t[r][c] != "0"); t[r][c] = "0"
json.dump(d, sys.stdout)' certs/fmm_3x3x3_23.json > certs/control_matmul_3x3x3_zeroed.json
t matmul-3x3x3 certs/control_matmul_3x3x3_zeroed.json "NOT CERTIFIED,"         # one coefficient set to 0
python3 -I -c 'import json, sys
d = json.load(open(sys.argv[1])); d["field"] = "GF(3)"; json.dump(d, sys.stdout)' certs/fmm_4x4x4_48.json > certs/control_matmul_4x4x4_gf3.json
t matmul-4x4x4 certs/control_matmul_4x4x4_gf3.json "NOT CERTIFIED,"            # characteristic 3 is not allowed here
sed '$d' certs/cook_monalisa_5757191.tour | sed '$d' > certs/control_monalisa_short.tour
t tsp-mona-lisa certs/control_monalisa_short.tour "NOT CERTIFIED,"              # a city left out
python3 -I -c 'import math
print("\n".join("%d %d" % (round(1000 * math.cos(2 * math.pi * k / 9)), round(1000 * math.sin(2 * math.pi * k / 9))) for k in range(9)))' > certs/control_convex_nonagon.txt
t erdos-107 certs/control_convex_nonagon.txt "NOT CERTIFIED,"                   # convex: not a counterexample
printf '0 1\n1 2\n2 3\n3 4\n' > certs/control_tree_path.txt
t erdos-993 certs/control_tree_path.txt "NOT CERTIFIED,"                        # a path: unimodal
python3 -I tests/units_prestige.py || status=1
if python3 -I tools/build_prestige100.py --check > /dev/null; then echo "ok    collections/prestige100 (100 problems, records agree with the problem files)"; else echo "FAIL  collections/prestige100"; status=1; fi
# checker unit tests: the exit status of a checker run on its own
u() {  # u EXPECTED_EXIT_STATUS CHECKER ARGS...
  want=$1; shift
  python3 -I "$@" > /dev/null 2>&1; got=$?
  if [ "$got" = "$want" ]; then echo "ok    unit $*: exit $got"; else echo "FAIL  unit $*: exit $got (expected $want)"; status=1; fi
}
u 0 checkers/hadamard_check.py 16 certs/unit_sylvester16.txt
sed '2s/^./-/' certs/unit_sylvester16.txt > certs/control_hadamard_flip.txt
u 1 checkers/hadamard_check.py 16 certs/control_hadamard_flip.txt
printf -- '-1 1 1 1\n' > certs/unit_cw_4_4.txt
u 0 checkers/cwm_check.py 4 4 certs/unit_cw_4_4.txt                             # the circulant Hadamard matrix of order 4
printf -- '-1 0 1 0 1 0 1 0\n' > certs/control_cw_8_4_improper.txt
u 1 checkers/cwm_check.py 8 4 certs/control_cw_8_4_improper.txt                 # W W^T = 4 I but not proper
u 0 checkers/cage_check.py 3 5 certs/control_cage_petersen.txt                   # the Petersen graph is a (3,5)-cage
u 0 checkers/degdiam_check.py 3 2 certs/control_cage_petersen.txt                # and a Moore graph of diameter 2
# v2.0: the checkers added or changed in v2.0 (ca_check.py, lincode_check.py, rcpsp_check.py, covering_check.py):
# known objects with their exact values, red controls and cross-checks against brute force; then a few sampled cells
# of every family (an object of ours for each, certified and not improving, and a red control refused); then
# index.json against the files it lists
python3 -I tests/units.py || status=1
python3 -I tests/sample_cells.py || status=1
if python3 -I obb.py index > /dev/null; then echo "ok    index.json matches the files"; else echo "FAIL  index.json"; status=1; fi
exit $status
