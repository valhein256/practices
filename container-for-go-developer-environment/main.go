package main

import (
	"fmt"
	"os"
	"strings"
	"sync"

	"github.com/pkg/errors"
)

func echo(args []string) error {
	if len(args) < 2 {
		return errors.New("no message to echo")
	}
	_, err := fmt.Println(strings.Join(args[1:], " "))
	return err
}

func main() {
	if err := echo(os.Args); err != nil {
		fmt.Fprintf(os.Stderr, "%+v\n", err)
	}

	pool_count := 10
	urls := []string{
		"google",
		"yahoo",
		"FB",
		"MSFT",
		"TESLA",
		"error",
	}
	var wg sync.WaitGroup
	inChan := make(chan string, len(urls))
	outChan := make(chan string)
	errChan := make(chan string)
	finishChan := make(chan struct{})
	wg.Add(pool_count)

	for i := 0; i < pool_count; i++ {
		go func(inChan <-chan string, outChan chan<- string, errChan chan<- string, wg *sync.WaitGroup) {
			defer wg.Done()
			for str := range inChan {
				if str != "error" {
					outChan <- str
				} else {
					errChan <- str
				}
			}
		}(inChan, outChan, errChan, &wg)
	}

	for _, url := range urls {
		inChan <- url
	}
	close(inChan)

	go func() {
		wg.Wait()
		close(finishChan)
	}()
	results := []string{}
	err_results := []string{}

Loop:
	for {
		select {
		case str := <-outChan:
			results = append(results, str)
		case str := <-errChan:
			err_results = append(err_results, str)
		case <-finishChan:
			break Loop
		}
	}

	fmt.Println(LICENSE_ID, VENDOR_ID, HOST)
	fmt.Println(results)
	fmt.Println(err_results)
}
