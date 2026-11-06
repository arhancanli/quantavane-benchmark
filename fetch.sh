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
