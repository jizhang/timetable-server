module.exports = {
  extends: ['standard', 'prettier'],
  overrides: [
    {
      extends: [
        'standard',
        'plugin:@typescript-eslint/recommended',
        'plugin:@typescript-eslint/recommended-requiring-type-checking',
        'plugin:react/recommended',
        'plugin:react/jsx-runtime',
        'plugin:react-hooks/recommended',
        'prettier',
      ],
      files: ['**/*.ts?(x)'],
      parser: '@typescript-eslint/parser',
      parserOptions: {
        tsconfigRootDir: __dirname,
        project: ['./tsconfig.json'],
      },
      plugins: ['@typescript-eslint'],
      rules: {
        '@typescript-eslint/no-misused-promises': ['error', { checksVoidReturn: false }],
      },
      settings: {
        react: {
          version: 'detect',
        },
      },
    },
  ],
}
