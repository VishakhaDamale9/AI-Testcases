# Frontend Documentation

Modern React frontend with TypeScript, Chakra UI, TanStack Router, and TanStack Query.

## 🚀 Quick Start

### Prerequisites

- Node.js 18 or higher
- npm or yarn package manager

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### Environment Configuration

Create a `.env` file in the frontend directory:

```bash
VITE_API_URL=http://localhost:8000
```

### Running the Development Server

```bash
# Start development server
npm run dev
```

The application will be available at http://localhost:5173

## 📜 Available Scripts

### Development

```bash
# Start development server with hot reload
npm run dev
```

### Building

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Code Quality

```bash
# Lint and format code
npm run lint
```

### API Client Generation

```bash
# Generate TypeScript client from OpenAPI spec
npm run generate-client
```

This generates type-safe API client code in `src/client/` based on the backend's OpenAPI specification.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable React components
│   │   ├── ui/             # UI components (Chakra UI based)
│   │   └── ...
│   ├── routes/              # Route components
│   │   ├── __root.tsx      # Root layout
│   │   ├── index.tsx       # Home page
│   │   └── ...
│   ├── client/              # Auto-generated API client
│   │   ├── services/       # API service functions
│   │   └── types/          # TypeScript types
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utility functions
│   └── main.tsx             # Application entry point
├── public/                  # Static assets
├── index.html               # HTML template
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
├── vite.config.ts           # Vite configuration
└── biome.json               # Biome linter configuration
```

## 🎨 UI Components

This project uses **Chakra UI** for the component library. Key features:

- Accessible components out of the box
- Dark mode support
- Responsive design utilities
- Customizable theme

### Using Chakra UI Components

```tsx
import { Button, Box, Heading } from '@chakra-ui/react'

function MyComponent() {
  return (
    <Box p={4}>
      <Heading>Hello World</Heading>
      <Button colorScheme="blue">Click me</Button>
    </Box>
  )
}
```

## 🔄 State Management

### TanStack Query

Used for server state management:

```tsx
import { useQuery } from '@tanstack/react-query'
import { UsersService } from '@/client/services'

function UserList() {
  const { data, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: () => UsersService.getUsers()
  })
  
  if (isLoading) return <div>Loading...</div>
  
  return <div>{/* Render users */}</div>
}
```

### TanStack Router

File-based routing with type safety:

```tsx
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/users')({
  component: UserList
})
```

## 🔌 API Integration

The frontend uses an auto-generated TypeScript client for type-safe API calls.

### Regenerate API Client

When the backend API changes:

```bash
# Make sure backend is running
# Then generate new client
npm run generate-client
```

### Using the API Client

```tsx
import { UsersService } from '@/client/services'

// Get all users
const users = await UsersService.getUsers()

// Create a user
const newUser = await UsersService.createUser({
  email: 'user@example.com',
  password: 'password123'
})
```

## 🎨 Styling

### Chakra UI Theme

Customize the theme in `src/theme/`:

```tsx
import { extendTheme } from '@chakra-ui/react'

const theme = extendTheme({
  colors: {
    brand: {
      500: '#3182ce'
    }
  }
})
```

### Dark Mode

Dark mode is supported out of the box with `next-themes`:

```tsx
import { useColorMode } from '@chakra-ui/react'

function ThemeToggle() {
  const { colorMode, toggleColorMode } = useColorMode()
  
  return (
    <Button onClick={toggleColorMode}>
      Toggle {colorMode === 'light' ? 'Dark' : 'Light'}
    </Button>
  )
}
```

## 🧪 Testing

### E2E Testing with Playwright

```bash
# Install Playwright browsers (first time only)
npx playwright install

# Run E2E tests
npx playwright test

# Run tests in UI mode
npx playwright test --ui
```

Test files are located in `tests/` directory.

## 🔧 Configuration

### TypeScript

TypeScript configuration is split across multiple files:
- `tsconfig.json`: Main TypeScript config
- `tsconfig.build.json`: Build-specific config
- `tsconfig.node.json`: Node.js specific config

### Vite

Vite configuration in `vite.config.ts`:
- React plugin with SWC
- TanStack Router plugin
- Path aliases
- Proxy configuration

## 📦 Key Dependencies

### Core
- **React**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server

### UI
- **Chakra UI**: Component library
- **React Icons**: Icon library
- **next-themes**: Theme management

### Routing & State
- **TanStack Router**: Type-safe routing
- **TanStack Query**: Server state management

### Forms
- **React Hook Form**: Form management

### API
- **Axios**: HTTP client
- **@hey-api/openapi-ts**: OpenAPI client generator

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

### Deploy to Hosting

The `dist/` folder can be deployed to any static hosting service:
- Vercel
- Netlify
- AWS S3 + CloudFront
- GitHub Pages
- etc.

## 🐛 Debugging

### React DevTools

Install the React DevTools browser extension for debugging React components.

### TanStack Query DevTools

The Query DevTools are automatically included in development mode. Look for the floating icon in the bottom corner of the app.

### TanStack Router DevTools

The Router DevTools are automatically included in development mode.

## 📚 Additional Resources

- [React Documentation](https://react.dev)
- [Chakra UI Documentation](https://chakra-ui.com)
- [TanStack Query Documentation](https://tanstack.com/query)
- [TanStack Router Documentation](https://tanstack.com/router)
- [Vite Documentation](https://vitejs.dev)
