# for windows
ifeq ($(OS),Windows_NT)
all:./GGanalysislib/bin/GGanalysis.dll ./GGanalysislib/bin/LuckyRank.dll
# GGanalysis.dll compile
./GGanalysislib/bin/GGanalysis.dll :./source/GGanalysis.o ./source/LuckyRank.o ./source/MyTools.o
	gcc -o ./GGanalysislib/bin/GGanalysis.dll ./source/GGanalysis.o ./source/LuckyRank.o ./source/MyTools.o -s -shared -Wl,--subsystem,windows
./source/MyTools.o: ./source/MyTools.c ./source/MyTools.h
	gcc -c -o ./source/MyTools.o ./source/MyTools.c -O2
./source/GGanalysis.o : ./source/GGanalysis.c ./source/GGanalysis.h
	gcc -c -o ./source/GGanalysis.o ./source/GGanalysis.c -O2 -D API_EXPORTS
./source/LuckyRank.o : ./source/LuckyRank.c ./source/LuckyRank.h
	gcc -c -o ./source/LuckyRank.o ./source/LuckyRank.c -O2 -D API_EXPORTS
# LuckRasnk.dll compile.All function in LuckRasnk.dll is included in GGanalysis.dll
./GGanalysislib/bin/LuckyRank.dll :./source/LuckyRank.o ./source/MyTools.o
	gcc -o ./GGanalysislib/bin/LuckyRank.dll ./source/LuckyRank.o ./source/MyTools.o -s -shared -Wl,--subsystem,windows
clean :
	del ./GGanalysislib/source/*.o


# for Linux and macOS
else
all:./GGanalysislib/bin/GGanalysis.so ./GGanalysislib/bin/LuckyRank.so
# GGanalysis.dll compile
./GGanalysislib/bin/GGanalysis.so :./source/GGanalysis.o ./source/LuckyRank.o ./source/MyTools.o
	gcc -shared -o ./GGanalysislib/bin/GGanalysis.so ./source/GGanalysis.o ./source/LuckyRank.o ./source/MyTools.o
./source/MyTools.o: ./source/MyTools.c ./source/MyTools.h
	gcc -c -o ./source/MyTools.o ./source/MyTools.c -O2
./source/GGanalysis.o : ./source/GGanalysis.c ./source/GGanalysis.h
	gcc -c -fPIC -o ./source/GGanalysis.o ./source/GGanalysis.c -O2 -D API_EXPORTS
./source/LuckyRank.o : ./source/LuckyRank.c ./source/LuckyRank.h
	gcc -c -fPIC -o ./source/LuckyRank.o ./source/LuckyRank.c -O2 -D API_EXPORTS
# LuckRasnk.dll compile.All function in LuckRasnk.dll is included in GGanalysis.dll
./GGanalysislib/bin/LuckyRank.so :./source/LuckyRank.o ./source/MyTools.o
	gcc -shared -o ./GGanalysislib/bin/LuckyRank.so ./source/LuckyRank.o ./source/MyTools.o
clean :
	rm ./GGanalysislib/source/*.o
endif