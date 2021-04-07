module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: ['prettier', 'plugin:vue/vue3-essential', '@vue/airbnb'],
  parserOptions: {
    parser: 'babel-eslint',
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-shadow': 'off',
    'template-curly-spacing': 'off',
    indent: [
      'error',
      2,
      {
        ignoredNodes: ['TemplateLiteral'],
      },
    ],
    'no-extend-native': 'off',
    'max-len': ['error', { code: 256 }],
    'no-plusplus': ['error', { allowForLoopAfterthoughts: true }],
    'func-names': 'off',
  },
};
