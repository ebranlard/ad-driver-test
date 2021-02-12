
# CASES= HorizontalAxis
# CASES= VerticalAxis
CASES= BAR

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


EXT=out
FAILFILE=FAIL


# all: run test
# all: start $(ALL-RULES) summary
all: start $(RUN-RULES)



clean-%: 
	rm $*/InitFiles/*.txt  | true
	rm $*/Gamma/*.txt      | true

start:
	@rm -f $(FAILFILE)

run: $(RUN-RULES)
test: $(TEST-RULES)

run-%: 
	@echo "------------------------- RUN $* ----------------------------------"
	cd $* && $(OPENFAST) Main_$*.dvr    
# 	cat VerticalAxis/Main_VerticalAxis.ech 
# 	cd $* && $(OPENFAST) Main_Not$*.fst  >OUT_NOTOVER
# 	cd $* && $(OPENFAST) Main_$*.fst     >OUT_OVER

test-%:
	@echo "------------------------- TEST $* ----------------------------------"
	@python Test.py $*/Main_$*_ref.$(EXT) $*/Main_$*.$(EXT) && { echo ""; } || { echo "Fail $*">> $(FAILFILE); }
	@python Test.py $*/Main_$*.AD_ref.$(EXT) $*/Main_$*.AD.$(EXT) && { echo ""; } || { echo "Fail $*">> $(FAILFILE); }

summary:
	@echo "------------------------- SUMMARY ----------------------------------"
	@test -e $(FAILFILE) && { echo "[FAIL]"; cat $(FAILFILE); exit 1; } || { echo "[ OK ]"; } 
