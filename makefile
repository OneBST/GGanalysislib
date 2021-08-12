./GGanalysislib/bin/GGanalysis.dll :./GGanalysislib/source/GGanalysis.o
	gcc -o ./GGanalysislib/bin/GGanalysis.dll ./GGanalysislib/source/GGanalysis.o -s -shared -Wl,--subsystem,windows
./GGanalysislib/source/GGanalysis.o : ./GGanalysislib/source/GGanalysis.c ./GGanalysislib/source/GGanalysis.h
	gcc -c -o ./GGanalysislib/source/GGanalysis.o ./GGanalysislib/source/GGanalysis.c -O2 -D API_EXPORTS
clean :
	del ./GGanalysislib/source/*.o