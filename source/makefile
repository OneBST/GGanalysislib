# for Windows
ifeq ($(OS),Windows_NT)
all:GGanalysis.dll LuckyRank.dll
# GGanalysis.dll compile
GGanalysis.dll :GGanalysis.o LuckyRank.o MyTools.o
	gcc -o GGanalysis.dll GGanalysis.o LuckyRank.o MyTools.o -s -shared -Wl,--subsystem,windows
MyTools.o: MyTools.c MyTools.h
	gcc -c -o MyTools.o MyTools.c -O2
GGanalysis.o : GGanalysis.c GGanalysis.h
	gcc -c -o GGanalysis.o GGanalysis.c -O2 -D API_EXPORTS
LuckyRank.o : LuckyRank.c LuckyRank.h
	gcc -c -o LuckyRank.o LuckyRank.c -O2 -D API_EXPORTS
# LuckRasnk.dll compile.All function in LuckRasnk.dll is included in GGanalysis.dll
LuckyRank.dll :LuckyRank.o MyTools.o
	gcc -o LuckyRank.dll LuckyRank.o MyTools.o -s -shared -Wl,--subsystem,windows
clean :
	del *.o

# for Linux and macOS
else
all:libGGanalysis.so
libGGanalysis.so :GGanalysis.o LuckyRank.o MyTools.o
	gcc -shared -o libGGanalysis.so GGanalysis.o LuckyRank.o MyTools.o
MyTools.o: MyTools.c MyTools.h
	gcc -c -fPIC -o MyTools.o MyTools.c -O2
GGanalysis.o : GGanalysis.c GGanalysis.h
	gcc -c -fPIC -o GGanalysis.o GGanalysis.c -O2
LuckyRank.o : LuckyRank.c LuckyRank.h
	gcc -c -fPIC -o LuckyRank.o LuckyRank.c -O2
clean :
	rm *.o
endif