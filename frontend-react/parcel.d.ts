declare module '*.module.css' {
  const styles: {
    [className: string]: string
  }
  export = styles
}

declare type GlobalFetch = WindowOrWorkerGlobalScope
