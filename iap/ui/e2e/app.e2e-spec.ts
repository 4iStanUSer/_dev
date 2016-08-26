import { IapPage } from './app.po';

describe('iap App', function() {
  let page: IapPage;

  beforeEach(() => {
    page = new IapPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
