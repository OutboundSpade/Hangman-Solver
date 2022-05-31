LD_FLAGS="-s -w"
all: build
build:
	go build -ldflags=${LD_FLAGS} -o cache_generator generator.go
