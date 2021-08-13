ifeq ($(OS),Windows_NT)
./GGanalysislib/bin/GGanalysis.dll :./source/GGanalysis.o
	gcc -o ./GGanalysislib/bin/GGanalysis.dll ./source/GGanalysis.o -s -shared -Wl,--subsystem,windows
./source/GGanalysis.o : ./source/GGanalysis.c ./source/GGanalysis.h
	gcc -c -o ./source/GGanalysis.o ./source/GGanalysis.c -O2 -D API_EXPORTS
clean :
	del ./GGanalysislib/source/*.o
else
./GGanalysislib/bin/libGGanalysis.so :./source/GGanalysis.o
	gcc -shared -o ./GGanalysislib/bin/libGGanalysis.so ./source/GGanalysis.o
./source/GGanalysis.o : ./source/GGanalysis.c ./source/GGanalysis.h
	gcc -c -fPIC -o ./source/GGanalysis.o ./source/GGanalysis.c -O2 -D API_EXPORTS
clean :
	rm ./GGanalysislib/source/*.o
endif