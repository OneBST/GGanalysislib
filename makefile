# for Windows
ifeq ($(OS),Windows_NT)
all:
	$(MAKE) -C .\source
	move .\source\GGanalysis.dll .\GGanalysislib\bin
	move .\source\LuckyRank.dll .\GGanalysislib\bin
clean:	
	$(MAKE) -C .\source clean
# for Linux and macOS
else
all:
	$(MAKE) -C ./source
	mv ./source/libGGanalysis.so ./GGanalysislib/bin
clean:	
	$(MAKE) -C ./source clean
endif
