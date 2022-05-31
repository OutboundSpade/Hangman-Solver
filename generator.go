package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

const (
	CACHE_VERSION = "1.0.0"
)

func main() {
	var (
		fileName         = flag.String("file", "", "file to read")
		ignoreApostrophe = flag.Bool("ignore-apos", false, "ignore apostrophe")
		outFile          = flag.String("out", ".words-cache", "output file")
	)
	flag.Parse()
	if *fileName == "" {
		fmt.Println("file name is required")
		os.Exit(1)
		return
	}
	if *outFile == "" {
		fmt.Println("out file is required")
		os.Exit(1)
		return
	}
	b, err := ioutil.ReadFile(*fileName)
	fmt.Printf("Reading file: %s\n", *fileName)
	if err != nil {
		fmt.Printf("Error reading file: %s\n", err)
		os.Exit(1)
		return
	}
	wordMap := make(map[int][]string)
	line := strings.Split(strings.Trim(string(b), " "), "\n")
	linelen := len(line)
	percentInterval := 2000
	wordCount := 0
	fmt.Printf("ignoring apostrophe: %t\n", *ignoreApostrophe)
	for i, aitem := range line {
		item := strings.Trim(aitem, " ")
		item = strings.Trim(aitem, "\r")
		item = strings.ToLower(aitem)
		if !(*ignoreApostrophe && strings.Contains(item, "'")) && !arrContains(wordMap[len(item)], item) {
			wordMap[len(item)] = append(wordMap[len(item)], item)
			wordCount++
		}
		if i%percentInterval == 0 {
			fmt.Printf("%f\n", float64(i)/float64(linelen)*100)
		}
	}

	fmt.Printf("Words:%d\n", wordCount)
	var o []byte
	o = append(o, []byte(fmt.Sprintf("Version: %s\n", CACHE_VERSION))...)
	o = append(o, []byte(fmt.Sprintf("Date: %s\n", time.Now()))...)
	o = append(o, []byte(fmt.Sprintf("WordCount: %d\n", wordCount))...)
	o = append(o, []byte(";\n")...)
	for len, i := range wordMap {
		if len == 0 {
			continue
		}
		o = append(o, []byte(fmt.Sprintf("%d\n;\n", len))...)
		for _, j := range i {
			o = append(o, []byte(j+"\n")...)
		}
		o = append(o, []byte(";\n")...)
	}
	ioutil.WriteFile(*outFile, o, 0644)
	fmt.Printf("Done\n")
}

func arrContains(a []string, s string) bool {
	for _, i := range a {
		if i == s {
			return true
		}
	}
	return false
}
