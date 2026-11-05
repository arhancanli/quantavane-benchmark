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
