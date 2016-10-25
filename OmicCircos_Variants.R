setwd("/Users/jacobreeves/Desktop/Tsai/poster/OmicCircos")

library(OmicCircos);
options(stringsAsFactors = FALSE);
seg_my = read.table ("Segement_arc.txt", sep="\t")

seg_my = cbind(seg_my,'NA','NA')
names(seg_my) = c("seg.name", "seg.Start", "seg.End","value")
seg.name1 <- paste("Chr0", c(1:9), sep="");
seg.name2 <- paste("Chr", c(10:19), sep="");
seg.name = c(seg.name1,seg.name2)
db       <- segAnglePo(seg.dat=seg_my,seg.name  )


arc_my = read.table ("Segement_arc.txt", sep="\t")
colnames (arc_my) =  c("chr" , "start" , "end" , "value" )


link_my_ori = read.table ("Ptrichocarpa_v3.0.vcf.txt", sep="\t")
link_my = link_my_ori[,c(1:3)]
colnames (link_my) =   c("seg1", "start1", "value")


link_my_ori2 = read.table ("P717_RNAseq_M201610_PASS.vcf.txt", sep="\t")
link_my2 = link_my_ori2[,c(1:3)]
colnames (link_my2) =   c("seg1", "start1", "value")


link_my_gff = read.table ("gff.txt", sep="\t")
gff = link_my_gff[,c(1:3)]
colnames (gff) =   c("seg1", "start1", "value")

colors  <- rainbow(19,alpha =0.5);


pdffile  <- "someTesting.pdf";
pdf(pdffile, 8, 8);

par(mar=c(2, 2, 2, 2));


plot(c(1,800), c(1,800), type="n", axes=FALSE, xlab="", ylab="", main="");

circos(R=370, xc=400, yc=400, cir=db, type="chr", col=colors, print.chr.lab=TRUE, W=8, scale=TRUE,side="out");

#circos(R=340,  xc=400, yc=400,cir=db, W=30, mapping = arc_my, col.v=3, type="arc2", col=c("black","grey"), B=FALSE, lwd=3);

circos(R=310,  xc=400, yc=400,cir=db, W=60, mapping=gff, type="l", col=colors[9], lwd=2);

circos(R=270,  xc=400, yc=400,cir=db, W=60, mapping=link_my2, type="l", col=colors[1], lwd=2);

#circos(R=230,  xc=400, yc=400,cir=db, W=60, mapping=link_my, type="l", col=colors[12], lwd=2);

circos(R=230,  xc=400, yc=400,cir=db, W=60, mapping=link_my2, type="l", col=colors[1], lwd=2);

circos(R=230,  xc=400, yc=400,cir=db, W=60, mapping=link_my, type="l", col=adjustcolor(colors[12], 0.3), lwd=2);

dev.off()

