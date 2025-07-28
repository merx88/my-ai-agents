# 트렌딩 스크래퍼

나무뉴스, 구글 실시간 검색어, X 에서 트렌드를 찾아 이유와 함께 마크다운으로 노션에 저장해주는 에이전트입니다

## 세팅

```bash
#LLM
MODEL="Model"
GEMINI_API_KEY="your_key"

# notion
NOTION_API_KEY = "your_key"
DATABASE_ID = "your_db_id"

#tavily
TAVILY_API_KEY="your_key"
```

## 실행

```bash
crewai run
```

## 결과

아래와 같은 형식으로 요약해줍니다.

```markdown
# Now Top3 Trends

## 1. Keyword: 최원준

**Why it's trending:** 최원준 is trending due to a recent trade in the Korean professional baseball league (KBO). He was involved in a 3-for-3 trade between KIA Tigers and NC Dinos.

## 2. Keyword: 구준엽

**Why it's trending:** 구준엽 (DJ Koo) is trending because of his continued devotion to his late wife, Taiwanese actress Barbie Hsu (서희원). News reports detail his daily routine of maintaining her belongings and the touching display of love.

## 3. Keyword: 차은우

**Why it's trending:** 차은우 (Cha Eun-woo) is currently trending because he has recently enlisted in the military. He entered the training center on July 28th and will serve in the army band after completing his basic training.
```

파일은 final.md로 제공됩니다.

> 스크래핑 결과들은 Ouput 폴더에 저장됩니다.

```markdown
./output
├── final.md
├── google.md
├── namunews.md
├── scrapped_site.md
├── trend.md
└── x.md
```

> ⚠️ **주의:** signal 스크래핑은 오류가 있어 현재 주석처리 되어있습니다.

