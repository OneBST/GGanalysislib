./bin/GGanalysis.dll :./source/GGanalysis.o
	gcc -o ./bin/GGanalysis.dll ./source/GGanalysis.o -s -shared -Wl,--subsystem,windows
./source/GGanalysis.o : ./source/GGanalysis.c ./source/GGanalysis.h
	gcc -c -o ./source/GGanalysis.o ./source/GGanalysis.c -O2 -D API_EXPORTS
clean :
	del ./source/*.o