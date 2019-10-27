export GO111MODULE=on

mod:
	go mod download

.PHONY:tools
tools:
	go install github.com/jessevdk/go-assets-builder \
		github.com/mitchellh/gox \
		github.com/tcnksm/ghr

test:
	go test -v -race ./...

test/e2e:
	go test -tags=e2e -timeout=30m -v -race ./...

gen:
	go generate ./rc

package: gen
	./scripts/package.sh

release: package
	./scripts/release.sh

dev-install:
	go install github.com/utahta/pythonbrew/cmd/pythonbrew

