import { IapPage } from './app.po';

describe('migration-proj App', function() {
  let page: IapPage;

  beforeEach(() => {
    page = new IapPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
