
CASES=
CASES+= EllipticalWingInf_OLAF
CASES+= BAR_OLAF
CASES+= HelicalWakeInf_OLAF
CASES+= VerticalAxis_OLAF
CASES+= Kite_OLAF
CASES+= MultipleHAWT
CASES+= BAR_SineMotion
CASES+= BAR_RNAMotion
# CASES= _XFlow
# CASES+= MultipleHAWT_OLAF
# CASES= DEBUG

ALL-RULES= $(foreach case,$(CASES), run-$(case) test-$(case))
RUN-RULES= $(foreach case,$(CASES), run-$(case))
TEST-RULES= $(foreach case,$(CASES), test-$(case))


SLASH=\\
ifeq ($(OS),Windows_NT)
    OS=Windows
    CMAKE_ARGS:=$(CMAKE_ARGS) -G"MinGW Makefiles"
    MAKE=make
    RMDIR=rmdir /S /Q
    LIBEXT=.dll
    EXEEXT=.exe
    COPY=copy /Y
    SLASH=\\
else
    OS=$(shell uname -s)
    ifeq ($(OS),Linux)
    	LIBEXT='.so'
    	LIBPRE='lib'
    else ifeq ($(OS),Darwin)
    	LIBEXT='.dylib'
    endif
    RMDIR=rm -rf
    COPY=cp
endif
# OPENFAST=../../openfast/build/glue-codes/openfast/openfast
OPENFAST=..$(SLASH)aerodynm_driver$(EXEEXT)


EXT=outb
FAILFILE=FAIL


# all: run test
all: start $(ALL-RULES) summary
# all: start $(RUN-RULES)

# all:
# 	./aerodynm_driver.exe _Xflow/Main__XFlow.dvr
# 
#./aerodynm_driver.exe _XflowParametric/0.dvr


clean-%: 
	rm $*/InitFiles/*.txt  | true
	rm $*/Gamma/*.txt      | true

start:
	@rm -f $(FAILFILE)

run: $(RUN-RULES)
test: $(TEST-RULES)

run-%: 
	@echo "------------------------- RUN $* ----------------------------------"
	@cd $* && rm -f Main_$*.out  || true
	@cd $* && rm -f Main_$*.outb  || true
	@cd $* && $(OPENFAST) Main_$*.dvr    
# 	cat VerticalAxis/Main_VerticalAxis.ech 
# 	cd $* && $(OPENFAST) Main_Not$*.fst  >OUT_NOTOVER
# 	cd $* && $(OPENFAST) Main_$*.fst     >OUT_OVER

test-%:
	@echo "------------------------- TEST $* ----------------------------------"
	@python Test.py $*/Main_$*_ref.$(EXT) $*/Main_$*.$(EXT) &&  echo "";  ||  echo "[FAIL] $*" >> $(FAILFILE); 

summary:
	@echo "------------------------- SUMMARY ----------------------------------"
	@test -e $(FAILFILE) &&  cat $(FAILFILE)  ||  echo "[ OK ] $(RUN-RULES)"; 
