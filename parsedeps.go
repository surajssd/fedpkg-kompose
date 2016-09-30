// Helper for parsing Godeps.json file and spitting out
// bundled provides statements for an rpm spec file.
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
)

type Dep struct {
	ImportPath string
	Comment    string
	Rev        string
}

type GoDeps struct {
	ImportPath   string
	GoVersion    string
	GodepVersion string
	Packages     []string
	Deps         []*Dep
}

func main() {
	var deps GoDeps
	var x []byte
	var err error

	deps = GoDeps{}
	if x, err = ioutil.ReadFile("Godeps.json"); err != nil {
		fmt.Println(err)
		return
	}

	// Read in the json data and parse into Go structures
	json.Unmarshal(x, &deps)

	// Iterate over the deps that were unmarshaled and print
	// out bundle information for each one.
	for _, v := range deps.Deps {
		fmt.Printf("Provides: bundled(golang(%s)) = %s-%s\n",
			v.ImportPath, "%{version}", v.Rev)
	}
}
