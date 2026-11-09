#!/bin/sh
# Reference submissions (the certificates behind the best values), each checked against its SHA-256.
set -e
mkdir -p certs && cd certs
get() { [ -s "$1" ] || curl -s -f -L -o "$1" "$2"; echo "$3  $1" | shasum -a 256 -c -; }
get kos_1c.json https://raw.githubusercontent.com/DennisKoshta/c1c-autocorrelation-certificate/a4ee94ef29ff/K24576_0.4103333.json 963cb7273062e7360fdfa460bb19c1cf37729364b8f708b09580b6655b783c9e
get vid_1c_v3.json https://raw.githubusercontent.com/vidigoat/optimization-records/42d6a89fab4b1714af3a98a6dd43368615052b45/tao/certificates/c1c_v3/c1c_K98304_v3.json e0786a59bd9d8598d9f4a86fcee40575ea108a97b184b332ef05bb6764caec66
get huiihao_1d.json https://raw.githubusercontent.com/huiihao/c1d-certificate/302817dc3227ce281e9cfb486f12ff0df7fe2876/construction.json c489b46b894358d8934b378a577c04bd442d5dc784799de62b61d2f79a0358df
get pin_68a.json https://raw.githubusercontent.com/rpinho/korenblum-c68-certificate/9d48de64987911f5a07a397323345be8b97770a8/certificate-jung.json 80a056f2cec4cfd933944fa51100bc5a1a9657f1a1de509e3a51401ff282002b
get vid_68a_044605.json https://raw.githubusercontent.com/vidigoat/optimization-records/1a76f9dd053d51cce531b57b2ad5a68e3205ca75/tao/certificates/c68/certificate-c044605.json b8ea516b0168b179fbfa36aad262e13c75fe544c616e03af121dec7c176a054d
get cremer_6_8_n134.txt https://raw.githubusercontent.com/fritzcremer/ramsey-lower-bounds/880b4fa5e683de842e514054da6edb8a5482ff4a/R6_8/n134-gpt-6.1-sol.txt 8ef378ad4d66478c33939e438d3a64572ec2cf7d1647ae29d3568817fedfc982
get griego_c42.json https://raw.githubusercontent.com/sebastian-griego/turan-c42-certificate/c8ddce14d9a5e898406d5dc6b8d08bb8a39507c7/certificate/turan42_certificate.json a76e913230028706416590367d86550d6834333041d21fc6635e09dc612e3a81
get pinho_c42_256.json https://raw.githubusercontent.com/rpinho/c42-certificate/a8a9bc309bd1992413fa07595bd60c5e3fa1b65b/certificates/c42_256.json 705a729155eb508878d17ebea0322627a0ae02451c044a346a99d2e81c7afcab
get gomyway_c59.json https://raw.githubusercontent.com/gomyway/c59-bohr-bidisc-certificate/a014dc9455815c2875507017ebcd303b8da27b63/c59_cert.json 6d2e39e8741fb5e73593d4db007c68831243d32fe4ae298bc4fe750033ebedab
# Leaps in Bounds certificates (MIT licence; github.com/daniel-munro/leaps-in-bounds at commit 4521e13, 8 Nov 2026):
# record witnesses, or weaker ones, for the snake, coil, cap set, superpermutation, Schur, weak Schur, van der Waerden,
# no-three-in-line and degree-diameter problems; each is replayed by our own checker in test.sh
get lib_snake-in-the-box-9-lower-191.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/snake-in-the-box/snake-in-the-box-9-lower-191.txt a9b63ff19ff4040271899ad246ddee7481c759e926fd67824bd9228fe047afc3
get lib_snake-in-the-box-10-lower-379.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/snake-in-the-box/snake-in-the-box-10-lower-379.txt 8c4b7a1b988f2439a0bb576436333c0febb589b0750cdc429cbe6e827544f129
get lib_snake-in-the-box-11-lower-750.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/snake-in-the-box/snake-in-the-box-11-lower-750.txt 5672fffe7f937e7dd1bace3e50af9ff49af0934c658412a4c16b183773709101
get lib_snake-in-the-box-12-lower-1480.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/snake-in-the-box/snake-in-the-box-12-lower-1480.txt 850d48bffbe72b3db3659a19da5c6d6be15b1849e90ed3922343961c72ec0e0d
get lib_snake-in-the-box-13-lower-2946.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/snake-in-the-box/snake-in-the-box-13-lower-2946.txt 8e09dcd43ce278f4f35944fb981049672b468dcb038c07d8981fb84d8a656d85
get lib_coil-in-the-box-9-lower-192.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/coil-in-the-box/coil-in-the-box-9-lower-192.txt c65739694005f4c4a3b94d29f023f9d7556a0e0644c4a157538ac565cbfa1700
get lib_coil-in-the-box-10-lower-374.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/coil-in-the-box/coil-in-the-box-10-lower-374.txt 36b5ff0144422cc3e349c76c4c9f72d287b715544c4fc0de3dcc315cd9a1b67e
get lib_coil-in-the-box-11-lower-740.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/coil-in-the-box/coil-in-the-box-11-lower-740.txt 5e5504722f2754296e8a6bbfd9f2d635925af39cd3b34c1b24c850f2ecbfe2cf
get lib_coil-in-the-box-12-lower-1468.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/coil-in-the-box/coil-in-the-box-12-lower-1468.txt 23d0735ea85d9e6714447a8109ed18e66c5828e9ae982caef814e364b91e3d22
get lib_coil-in-the-box-13-lower-2930.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/coil-in-the-box/coil-in-the-box-13-lower-2930.txt c66196b93ed07d7683390139a0cfd15dbe8017fb1abc809ee2dbec9b02867614
get lib_cap-set-7-lower-236.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/cap-set/cap-set-7-lower-236.txt 3c3fc5029a61be80a95714007fe9e9cc5574779284b65bbb846dd8421f019520
get lib_cap-set-8-lower-512.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/cap-set/cap-set-8-lower-512.txt 238d59d3199bd3f71861a2d44b477ea403ef9d588ede01062b216345949eaa0c
get lib_minimal-superpermutation-6-upper-873.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/minimal-superpermutation/minimal-superpermutation-6-upper-873.txt a508dbc423f21452afeb74f215b4620b4030366a5a5a30ddc99754add1f12883
get lib_minimal-superpermutation-7-upper-5913.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/minimal-superpermutation/minimal-superpermutation-7-upper-5913.txt 74783e4b39fc00308c5b0c3f6339135313c3497fa2686338edbdbf7b460f0b86
get lib_schur-6-lower-537.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/schur/schur-6-lower-537.txt c6266f6d369e86f515b21f2cbc78bc4449366c39c26813df67d82e08a7e13b6b
get lib_schur-7-lower-1696.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/schur/schur-7-lower-1696.txt 6d4794df0f86e60e60aa3f8b33af2ba5a989bd03fdeea2c39637c4f735b54650
get lib_schur-8-lower-5372.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/schur/schur-8-lower-5372.txt 53a3bd0ea674aedb6d184ab630ff4fdb19f490bc4590cd9cad52c8573da73583
get lib_weak-schur-5-lower-207.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/weak-schur/weak-schur-5-lower-207.txt e35bcbb75659616a3be80e6d572b1e3ec010cecdc8a7d8f3043226417b47f463
get lib_weak-schur-6-lower-650.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/weak-schur/weak-schur-6-lower-650.txt 300891d3d3387bee9684c1673d9b329ecd75df37affd88b7060d42c6e235c96f
get lib_van-der-waerden-2-7-lower-3704.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/van-der-waerden/van-der-waerden-2-7-lower-3704.txt efebc0141a14f58698916c0220971e3290f29ed012f29248cddb8ebc22402d29
get lib_van-der-waerden-2-8-lower-11496.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/van-der-waerden/van-der-waerden-2-8-lower-11496.txt 52e5dd8262f9cbac0ada4e5fc5e8f95de35491c04471d9c2fce6c4f4121e1357
get lib_van-der-waerden-4-4-lower-1049.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/van-der-waerden/van-der-waerden-4-4-lower-1049.txt 06af9ae6792406160a632001430f59ab4d0ddad7f66dc674782db30870ab263c
get lib_van-der-waerden-4-5-lower-17706.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/van-der-waerden/van-der-waerden-4-5-lower-17706.txt eafdaebaecfd9a8ccefc2ad14d9b6ca1af7f3829fe34a31c0d8d848c93ed98e5
get lib_van-der-waerden-5-4-lower-2255.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/van-der-waerden/van-der-waerden-5-4-lower-2255.txt 8bfa63f2bb1c217d5151107060e1824c802f7e533f3c0ac62853cafe3027f06f
get lib_van-der-waerden-6-4-lower-9779.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/van-der-waerden/van-der-waerden-6-4-lower-9779.txt a6cfcc22c7177c774c1821bb24463660cc011ae770b543d657fc384a281f3b4f
get lib_no-three-in-line-75-lower-148.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/no-three-in-line/no-three-in-line-75-lower-148.txt 3dd21be9210fb79b9fd4fe188964ecf9340ff6a1ddaf1a23a06facb4732809ac
get lib_no-three-in-line-77-lower-152.txt https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/no-three-in-line/no-three-in-line-77-lower-152.txt 33e065a1e3ffcf2510c9a5095c38ab99970c235ff31397dac2c58a1ef569ffee
get lib_degree-diameter-3-5-lower-64.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-3-5-lower-64.s6 8fb5d6fa0c3d7bd416a39d8e1116ba4baf5740325eeb0b0ba05464535f936d2a
get lib_degree-diameter-3-6-lower-64.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-3-6-lower-64.s6 8fb5d6fa0c3d7bd416a39d8e1116ba4baf5740325eeb0b0ba05464535f936d2a
get lib_degree-diameter-3-7-lower-162.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-3-7-lower-162.s6 fe09ea11338cdcfc65d19d164ce0c9f20d165d0559ef213097f2cd6d16d68917
get lib_degree-diameter-3-8-lower-272.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-3-8-lower-272.s6 529a8decfedf934fbaf92772cb7c50dc2e644ef41d4ac3f8d2d2ea816d1ffcb4
get lib_degree-diameter-3-9-lower-506.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-3-9-lower-506.s6 aa461a85ed0bf00aa13bd608960b3ea10f2f2463c61ed79c3897d8d3c740ddd9
get lib_degree-diameter-3-10-lower-820.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-3-10-lower-820.s6 b52cd06dc716bb36ca3ffc899012913b7220a9cc31aacc67af51be1cd04991e2
get lib_degree-diameter-4-3-lower-41.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-4-3-lower-41.s6 72f1be69af439755e5f7ffce1b43dc9fe0431d555ce2dd189da2976c23935d70
get lib_degree-diameter-4-4-lower-84.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-4-4-lower-84.s6 442ac9d6b83f976e88a64ae259ee7a037b0854c5c4c749c1007d7f0ddbd25f7d
get lib_degree-diameter-4-5-lower-205.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-4-5-lower-205.s6 22574ceafde9293cc14920d73196b5668cc7f90239c68848e22a65cf2f572a9e
get lib_degree-diameter-5-3-lower-54.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-5-3-lower-54.s6 2eefb6e90c556f4e2c004f5fcd1546e53e820fc4d1d7cc41a5d1fee0fb613ff8
get lib_degree-diameter-5-4-lower-210.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-5-4-lower-210.s6 eee9d2cae6fe20a7dc1c0fd15c478c0189005a084ed5f9a2b409dfe7b8a3fa32
get lib_degree-diameter-8-2-lower-57.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-8-2-lower-57.s6 f14a5ac69f473deb556800344e4f507c1b44070c4b505d38e4327db7a32ae98e
get lib_degree-diameter-8-3-lower-253.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-8-3-lower-253.s6 b3bb2e8890d86d08a43814c8191acca9335cd7431f884832eeecbee4aa5e0285
get lib_degree-diameter-8-4-lower-1029.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-8-4-lower-1029.s6 7cfb70eb4d4792721190fedf0ba514aea9d1d2232ad9ecfaf7ceeeb295ab01c1
get lib_degree-diameter-9-3-lower-256.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-9-3-lower-256.s6 9dba1fbc8d7967e7d939363713ca4f3c3cef055dfb00580f088610634b6615d8
get lib_degree-diameter-10-2-lower-91.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-10-2-lower-91.s6 10b79e12bf5889b01350f3f49356c1ac63fcf79a046f0b217f7155c375671b2f
get lib_degree-diameter-10-3-lower-366.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-10-3-lower-366.s6 0460bb1f355ed9815599e0d3075c4bfc6635a1efbd646e6f41211b5611932961
get lib_degree-diameter-11-3-lower-420.s6 https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/4521e13522e0e191ed2212eda9f00a870fde1d7c/certificates/degree-diameter/degree-diameter-11-3-lower-420.s6 74df5dc2ad11eaa269a61ef0851335ba7eeb24467c3195863b9e8c8e4859a85a

# v2.1, Quantavane Prestige 100 (collections/prestige100): the Mona Lisa instance and record certificates, replayed by
# our checkers in test.sh. Data only; tools/convert_certs.py turns them into our checkers' formats.
mkdir -p ../instances/tsp
get ../instances/tsp/mona-lisa100K.tsp https://www.math.uwaterloo.ca/tsp/data/ml/mona-lisa100K.tsp 532fefbfb9ad66cc2550bece766fa069acaa8e34ee511ac1949ae101da4d70ad
get cook_monalisa_5757191.tour https://www.math.uwaterloo.ca/tsp/data/ml/tour/monalisa_5757191.tour d8a98a936d01b0317ff63a43646fbbbfa74bf6ee954a9449ad659128e579eb88
get fmm_3x3x3_tensor.mpl.bz2 https://fmm.univ-lille.fr/3x3x3_tensor.mpl.bz2 c145cff7708b8472de23e0112c0722cae05f08bed2d9883b8dbf98cbb843169e
get fmm_4x4x4_tensor.mpl.bz2 https://fmm.univ-lille.fr/4x4x4_tensor.mpl.bz2 5e6c6488e9982961d8d476dcc09972ce7de7a74a1deb0c913fbd309679ba2c49
get dobbelaere_sorting_networks_6bb0bd2.html https://raw.githubusercontent.com/bertdobbelaere/bertdobbelaere.github.io/6bb0bd2cb560064a1d92f35513dfed974e098eb1/sorting_networks.html fb08a5cd90a460607586be0f753fa19baedc1e5fe1c7d4247efc1923e6dfd0f6
get mckenna_schur6-538.word https://raw.githubusercontent.com/mysticflounder/schur-538/ebc5f5598881eded8c053b0ffe3a712d3e55f4b2/schur6-538.word 9e149c007b778655afd199685ebcc76260604a44f4c322d8aa9a1d96afb71d20
get ours_c1a_upper_n262144.json https://raw.githubusercontent.com/arhancanli/quantavane-replays/c40060ff2d03ed022d970ef25047e70c23a54ad3/improvements/c1a/c1a_upper_n262144.json a5eba0bf61429955a179b8d436fd72d2934a7b1677cedec333bec2f381f85361
L=https://raw.githubusercontent.com/daniel-munro/leaps-in-bounds/a5bbf82e21aa362df89d634c3cd79e3109674ac8/certificates
get lib_ramsey-6-6-lower-102.g6 $L/ramsey/ramsey-6-6-lower-102.g6 ebc60e8269cb2c447fe1ba42c3c8d05c788e130cdd0f63e82ca91e2d00635353
get lib_ramsey-7-7-lower-205.g6 $L/ramsey/ramsey-7-7-lower-205.g6 6d87bee01a7eea3646d0198740c35b6e550dcc234635c251ae045279299ec06d
get lib_ramsey-8-8-lower-282.g6 $L/ramsey/ramsey-8-8-lower-282.g6 4ab78933e6b619ba7bab6f1d6f1b9c740492a2322bfb2445a168a02d48fc978d
get lib_weak-schur-7-lower-2154.txt $L/weak-schur/weak-schur-7-lower-2154.txt c05c5cd24de7302904c08a1d618f585cee512b0622a76e22fc75839a7a9dfaab
get lib_weak-schur-8-lower-7002.txt $L/weak-schur/weak-schur-8-lower-7002.txt c2d529a4f41b380756f94f091a86a99489d8ee819b3c5d68c8fa4253d04ae0ab
get lib_weak-schur-9-lower-22620.txt $L/weak-schur/weak-schur-9-lower-22620.txt 5b6e7c96b0a800a77f12facfc2fc197a49cfb72d9e867a9bbac64951625ef5ad
C="python3 -I ../tools/convert_certs.py"
[ -s fmm_3x3x3_23.json ] || $C fmm fmm_3x3x3_tensor.mpl.bz2 fmm_3x3x3_23.json 1
[ -s fmm_4x4x4_48.json ] || $C fmm fmm_4x4x4_tensor.mpl.bz2 fmm_4x4x4_48.json 1
for nw in 13:45 14:51 15:56 16:60 17:71; do
  n=${nw%:*}; s=${nw#*:}
  [ -s dobb_n${n}_s${s}.txt ] || $C dobbelaere dobbelaere_sorting_networks_6bb0bd2.html $n $s dobb_n${n}_s${s}.txt
done
for g in ramsey-6-6-lower-102 ramsey-7-7-lower-205 ramsey-8-8-lower-282; do
  [ -s derived_lib_$g.txt ] || $C g6 lib_$g.g6 derived_lib_$g.txt
done
[ -s derived_mckenna_schur6_538.txt ] || $C shift mckenna_schur6-538.word derived_mckenna_schur6_538.txt 1

# CVRPLIB instances for the routing problems, one request every 2 seconds
cd .. && mkdir -p instances && cd instances
slow() { [ -s "$1" ] || sleep 2; get "$@"; }
slow Antwerp1.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/258 f9206ba0037ccffea614cefb2300830b171ee192b4116a3c7a949f456d7870ff
slow Antwerp2.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/259 26b6ca241f76bc7993bc88faac4a0035e39ba93b24dcedd289f394be128f37da
slow Brussels1.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/260 df36365400cbc0dac8ba7d55f62234801519d29629d41c473f405419d8947503
slow Brussels2.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/261 1ae2a871fed6baff273bd3f6d869c272b0373a04acac7be3b919a90c98a9cd21
slow Flanders1.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/262 4b64deac4878d0cfdf3221195eacf794e8c45b91f18efc4eb26830b63193c3ab
slow Flanders2.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/263 2927e79b46b156a29ee45bb0c130f667bb9077fd2895fb1e99a2151665eaa68e
slow Ghent1.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/264 fff572e192410999fc8fb71e656728899b8ba1555f96bfb1d13a2c9114a11276
slow Ghent2.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/265 a07c1c03491527f5c1890230ceab59cfd2e67a01d362c4c7d03b4515fc7a001a
slow Leuven2.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/267 dbcf78551e64f523d3ad535ff04fd3be2c8bb21dc704e9053fccb18d20201b9a
slow XL-n1048-k237.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/280 3718a537257b90d30d5dfc111739098b4aa7c8ecf5cac48232f77fb2eef4907c
slow XL-n1748-k271.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/295 ed4d6e78f738af93892fe15da80ae6e2572b628fd8816e6ad032fefc709f3e97
slow XL-n6168-k1922.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/357 55b0f0a1fe0793feed56cbd261a431808f65b88a7207cdc5ee59cff95ad8162e
slow XL-n8028-k294.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/369 680f7815f0633a6e1786079985060534da9d6ea8010a3a7900befda6512df227
slow XL-n9784-k2774.vrp https://galgos.inf.puc-rio.br/cvrplib/en/download/instance/378 a29f80c7bd223c15301467a3778927e48e726a88e2d0e15574543d26a818d38a
