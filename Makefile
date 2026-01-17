UID := $(shell id -u)
GID := $(shell id -g)
export UID
export GID

help: ## このヘルプを表示
	@grep -E '^[a-zA-Z0-9_.-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS=":.*## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' ## ターゲット一覧

build: ## Docker開発イメージをビルド
	@docker compose -f compose.yml build ## 開発イメージをビルド

prepare: ## 実行前のローカルディレクトリ準備
	@mkdir -p logs ## ログ出力用ディレクトリ

test: prepare ## テストを実行
	@docker compose -f compose.yml run --rm python pytest -v | tee logs/test-$(shell date +%Y%m%d_%H%M%S).log ## テストログを保存

test-cov: prepare ## カバレッジ付きでテストを実行
	@docker compose -f compose.yml run --rm python pytest -v --cov=src --cov-report=term-missing | tee logs/test-cov-$(shell date +%Y%m%d_%H%M%S).log ## カバレッジ測定

run: prepare ## アプリを実行
	@docker compose -f compose.yml run --rm python python src/app.py ## アプリ実行

debug: prepare ## デバッグ起動（Attach待ち）
	@docker compose -f compose.yml run --rm --service-ports python-debug ## デバッグ起動

shell: prepare ## コンテナ内でシェルを起動
	@docker compose -f compose.yml run --rm python bash ## シェル起動

clean: prepare ## 実行キャッシュを削除
	@docker compose -f compose.yml run --rm python bash -lc "rm -rf .pytest_cache .coverage htmlcov logs/*.log && find src tests -name __pycache__ -type d -prune -exec rm -rf {} +" ## 生成物削除
