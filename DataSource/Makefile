VERSION_STRING = 0.84

sources = cyclictest.c data_source.c

TARGETS = $(sources:.c=)

LIBS 	= -lrt -lpthread -lrttest -L.
EXTRA_LIBS ?= -ldl	# for get_cpu
DESTDIR	?=
prefix  ?= /usr/local
bindir  ?= $(prefix)/bin
mandir	?= $(prefix)/share/man
srcdir	?= $(prefix)/src

machinetype = $(shell $(CC) -dumpmachine | \
    sed -e 's/-.*//' -e 's/i.86/i386/' -e 's/mips.*/mips/' -e 's/ppc.*/powerpc/')
ifneq ($(filter x86_64 i386 ia64 mips powerpc,$(machinetype)),)
NUMA 	:= 1
endif

CFLAGS ?= -D_GNU_SOURCE -Wall -Wno-nonnull -Isrc/include
LDFLAGS ?=

PYLIB  := $(shell python -c 'import distutils.sysconfig;  print distutils.sysconfig.get_python_lib()')

ifndef DEBUG
	CFLAGS	+= -O2
else
	CFLAGS	+= -O0 -g
endif

ifeq ($(NUMA),1)
	CFLAGS += -DNUMA
	NUMA_LIBS = -lnuma
endif

VPATH	= src/cyclictest:
VPATH	+= src/data_source:
VPATH	+= src/pi_tests:
VPATH	+= src/lib

%.o: %.c
	$(CC) -D VERSION_STRING=$(VERSION_STRING) -c $< $(CFLAGS)

# Pattern rule to generate dependency files from .c files
%.d: %.c
	@$(CC) -MM $(CFLAGS) $< | sed 's,\($*\)\.o[ :]*,\1.o $@ : ,g' > $@ || rm -f $@

.PHONY: all
all: $(TARGETS) hwlatdetect

# Include dependency files, automatically generate them if needed.
-include $(sources:.c=.d)

cyclictest: cyclictest.o librttest.a
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LIBS) $(NUMA_LIBS)

data_source: data_source.o
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LIBS) $(NUMA_LIBS)

# pi_stress: pi_stress.o
# 	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LIBS)

hwlatdetect:  src/hwlatdetect/hwlatdetect.py
	chmod +x src/hwlatdetect/hwlatdetect.py
	ln -s src/hwlatdetect/hwlatdetect.py hwlatdetect

# pip_stress: pip_stress.o librttest.a
# 	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LIBS)

librttest.a: rt-utils.o error.o rt-get_cpu.o
	$(AR) rcs librttest.a rt-utils.o error.o rt-get_cpu.o

CLEANUP  = $(TARGETS) *.o .depend *.*~ *.orig *.rej rt-tests.spec *.d *.a
CLEANUP += $(if $(wildcard .git), ChangeLog)

.PHONY: clean
clean:
	for F in $(CLEANUP); do find -type f -name $$F | xargs rm -f; done
	rm -f hwlatdetect
	rm -f tags
	rm -f histogram output
.PHONY: distclean
distclean: clean
	rm -rf BUILD RPMS SRPMS releases *.tar.gz rt-tests.spec

.PHONY: changelog
changelog:
	git log >ChangeLog

.PHONY: install
install: all
	mkdir -p "$(DESTDIR)$(bindir)" "$(DESTDIR)$(mandir)/man4"
	mkdir -p "$(DESTDIR)$(srcdir)" "$(DESTDIR)$(mandir)/man8"
	cp $(TARGETS) "$(DESTDIR)$(bindir)"
	if test -n "$(PYLIB)" ; then \
		install -D -m 755 src/hwlatdetect/hwlatdetect.py $(DESTDIR)$(PYLIB)/hwlatdetect.py ; \
		rm -f "$(DESTDIR)$(bindir)/hwlatdetect" ; \
		ln -s $(PYLIB)/hwlatdetect.py "$(DESTDIR)$(bindir)/hwlatdetect" ; \
	fi
	gzip src/cyclictest/cyclictest.8 -c >"$(DESTDIR)$(mandir)/man8/cyclictest.8.gz"
	# gzip src/pi_tests/pi_stress.8 -c >"$(DESTDIR)$(mandir)/man8/pi_stress.8.gz"
	gzip src/hwlatdetect/hwlatdetect.8 -c >"$(DESTDIR)$(mandir)/man8/hwlatdetect.8.gz"

.PHONY: release
release: clean changelog
	mkdir -p releases
	rm -rf tmp && mkdir -p tmp/rt-tests
	cp -r Makefile COPYING ChangeLog src tmp/rt-tests
	tar -C tmp -czf rt-tests-$(VERSION_STRING).tar.gz rt-tests
	rm -f ChangeLog
	cp rt-tests-$(VERSION_STRING).tar.gz releases

.PHONY: push
push:	release
	scripts/do-git-push $(VERSION_STRING)

.PHONY: pushtest
pushtest: release
	scripts/do-git-push --test $(VERSION_STRING)

rt-tests.spec: Makefile rt-tests.spec-in
	sed s/__VERSION__/$(VERSION_STRING)/ <$@-in >$@

HERE	:=	$(shell pwd)
RPMARGS	:=	--define "_topdir $(HERE)" 	\
		--define "_sourcedir $(HERE)/releases" 	\
		--define "_builddir $(HERE)/BUILD" 	\

.PHONY: rpm
rpm:	rpmdirs release rt-tests.spec
	rpmbuild -ba $(RPMARGS) rt-tests.spec

.PHONY: rpmdirs
rpmdirs:
	@[ -d BUILD ]  || mkdir BUILD
	@[ -d RPMS ]   || mkdir RPMS
	@[ -d SRPMS ]  || mkdir SRPMS

.PHONY: help
help:
	@echo ""
	@echo " rt-tests useful Makefile targets:"
	@echo ""
	@echo "    all       :  build all tests (default"
	@echo "    install   :  install tests to local filesystem"
	@echo "    release   :  build source tarfile"
	@echo "    rpm       :  build RPM package"
	@echo "    clean     :  remove object files"
	@echo "    distclean :  remove all generated files"
	@echo "    help      :  print this message"

.PHONY: tags
tags:
	ctags -R --extra=+f --c-kinds=+p *
