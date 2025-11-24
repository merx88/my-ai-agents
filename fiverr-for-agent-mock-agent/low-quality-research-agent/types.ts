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

export interface LowQualityGraphState {
  topic: string;
  results?: SearchResult[];
  scraped?: ScrapedPage[];
  summary?: string;
}
