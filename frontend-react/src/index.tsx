import * as ReactDOM from 'react-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import App from './App'

const queryClient = new QueryClient()
const app = document.getElementById('app')
ReactDOM.render(
  <QueryClientProvider client={queryClient}>
    <App />
  </QueryClientProvider>,
  app
)
