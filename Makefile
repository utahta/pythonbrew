
setup:
	@go get github.com/jessevdk/go-assets-builder
	@go get github.com/mitchellh/gox
	@go get github.com/tcnksm/ghr
	@dep ensure

test:
	@go test -v -race ./...

test/e2e:
	@go test -tags=e2e -v -race ./...

gen:
	@go generate ./rc

package: gen
	@./scripts/package.sh

release: package
	@./scripts/release.sh

