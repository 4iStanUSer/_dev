import { TestAngularCliBeta21Page } from './app.po';

describe('test-angular-cli-beta-21 App', function() {
  let page: TestAngularCliBeta21Page;

  beforeEach(() => {
    page = new TestAngularCliBeta21Page();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
