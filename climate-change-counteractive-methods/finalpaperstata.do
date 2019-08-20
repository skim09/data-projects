import delimited \\Client\C$\Users\swkim728\Desktop\wesleyan\fall_2018\econ300\final_project\recs2015_public_v3.csv, varnames(1) clear

replace tempgoneac =. if tempgoneac == -2
replace cooltype=. if cooltype==-2

table(cooltype)
table(numcfan)


reg dolelcol tempgoneac i.cooltype
reg dolelcol tempgoneac i.numcfan
