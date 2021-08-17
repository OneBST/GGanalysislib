# for windows
ifeq ($(OS),Windows_NT)
all:./GGanalysislib/bin/GGanalysis.dll ./GGanalysislib/bin/LuckyRank.dll
# GGanalysis.dll compile
./GGanalysislib/bin/GGanalysis.dll :./source/GGanalysis.o ./source/LuckyRank.o
	gcc -o ./GGanalysislib/bin/GGanalysis.dll ./source/GGanalysis.o ./source/LuckyRank.o -s -shared -Wl,--subsystem,windows
./source/GGanalysis.o : ./source/GGanalysis.c ./source/GGanalysis.h
	gcc -c -o ./source/GGanalysis.o ./source/GGanalysis.c -O2 -D API_EXPORTS
./source/LuckyRank.o : ./source/LuckyRank.c ./source/LuckyRank.h
	gcc -c -o ./source/LuckyRank.o ./source/LuckyRank.c -O2 -D API_EXPORTS
# LuckRasnk.dll compile.All function in LuckRasnk.dll is included in GGanalysis.dll
./GGanalysislib/bin/LuckyRank.dll :./source/LuckyRank.o
	gcc -o ./GGanalysislib/bin/LuckyRank.dll ./source/LuckyRank.o -s -shared -Wl,--subsystem,windows
clean :
	del ./GGanalysislib/source/*.o

# for Linux and macOS
else
./GGanalysislib/bin/libGGanalysis.so :./source/GGanalysis.o
	gcc -shared -o ./GGanalysislib/bin/libGGanalysis.so ./source/GGanalysis.o
./source/GGanalysis.o : ./source/GGanalysis.c ./source/GGanalysis.h
	gcc -c -fPIC -o ./source/GGanalysis.o ./source/GGanalysis.c -O2 -D API_EXPORTS
clean :
	rm ./GGanalysislib/source/*.o
endif