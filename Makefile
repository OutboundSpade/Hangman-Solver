all: build move
build:
	go build generator.go
move:
	mv generator cache_generator
