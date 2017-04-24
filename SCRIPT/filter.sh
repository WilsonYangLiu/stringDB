# This scirpt output 2 files: Ensemble.ENSP2ENSG.tsv; link.higher9.ENSP.tsv

cntDir=`pwd`
targetDir=/media/wilson/b776f228-366c-4e52-acd6-65df5b458e8c/Project_G/db.STRING
ProteinAlias=9606.protein.aliases.v10.txt.gz
Interaction=9606.protein.links.v10.txt.gz

cd $targetDir
# Get possible source of the object that match 'ENSG'
gzip -cd ./2.Association.Data/$ProteinAlias | grep 'ENSG' | awk -F "\t" '{print $3}' | sort | uniq
# Output: 
#Ensembl Ensembl_ArrayExpress (5000)
#Ensembl Ensembl_ArrayExpress Ensembl_HGNC_Ensembl_Gene_ID (15457)
#Ensembl_HGNC_Ensembl_Gene_ID (12)

# count the number of object belong to different source, with the matched pattern - '\b[Ee]nsembl\b'
gzip -cd ./2.Association.Data/$ProteinAlias | grep '\b[Ee]nsembl\b' | awk -F "\t" '{print $3}' | sort | \
awk '
BEGIN{FS="\s";OFS="\t";
   a="Ensembl";na=0;
   b="Ensembl Ensembl_ArrayExpress";nb=0
   c="Ensembl Ensembl_ArrayExpress Ensembl_HGNC_Ensembl_Gene_ID";nc=0
   d="Ensembl ensembl.org";nd=0};
{if ($0==a) 
   na=na+1;
else if ($0==b)
   nb=nb+1;
else if ($0==c)
   nc=nc+1
else if ($0==d)
   nd=nd+1}
END{print na,nb,nc,nd}' 
# Output: 221290   5000   15457   20457

# get Mapping between Eesemble gene id and STRING protein id
gzip -cd ./2.Association.Data/$ProteinAlias | grep 'ENSG.*\b[Ee]nsembl\b' | \
awk '
BEGIN{FS="\t";OFS="\t"};
{
   split($1,arr,".");
   print arr[2],$2}' > Ensemble.ENSP2ENSG.tsv

# get Links (filtered links) that not less than 900 (0.9)
gzip -cd ./1.Interaction.Data/$Interaction | awk '
BEGIN{FS=" ";OFS="\t"};
(NR>1){
if($3>=900){
   split($1,arr1,".");
   split($2,arr2,".");
   print arr1[2],arr2[2],$3}}
' | sort > link.higher9.ENSP.tsv

# count the number of filtered links
gzip -cd ./1.Interaction.Data/$Interaction | awk '
BEGIN{FS=" ";OFS="\n"};
(NR>1){
if($3>=900){
   split($1,arr1,".");
   split($2,arr2,".");
   print arr1[2],arr2[2]}}
' | sort | uniq | wc -l
# Output: 11132

:<<BLOCK
# Skip the following steps
# count the number of the unique ensemble gene id
wc -l gencode.v22.annotation.used4FPKM.csv
# Output 60484 (plus header)

# Get the mapping of ensemble gene id (without verson suffix) and gene symbol 
cat gencode.v22.annotation.used4FPKM.csv | awk '
BEGIN{FS=",";OFS="\t"};
(NR>1){
   split($1,arr,".");
   print arr[1],arr[2],$2}' > gencode.v22.annotation.tsv

BLOCK
cd $cntDir

