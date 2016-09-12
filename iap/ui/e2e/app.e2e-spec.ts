import { AngularCliWebpack8Page } from './app.po';

describe('angular-cli-webpack-8 App', function() {
  let page: AngularCliWebpack8Page;

  beforeEach(() => {
    page = new AngularCliWebpack8Page();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
