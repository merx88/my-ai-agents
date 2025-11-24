// types.ts
export interface SearchResult {
  url: string;
  title?: string;
  snippet?: string;
}

export interface ScrapedPage {
  url: string;
  title?: string;
  content: string;
}

export interface PageSummary {
  url: string;
  title?: string;
  summary: string;
}

export interface HighQualityGraphState {
  topic: string;
  results?: SearchResult[];
  scraped?: ScrapedPage[];
  pageSummaries?: PageSummary[];
  finalReport?: string; // 최종 하이퀄리티 리포트
}
