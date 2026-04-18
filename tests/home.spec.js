const { test, expect } = require("@playwright/test");

test.describe("Claude Opus 4.7 editorial site", () => {
  test("desktop homepage renders SEO content and internal navigation", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle(/Claude Opus 4\.7 Review/i);
    await expect(page.locator("h1")).toHaveText("Claude Opus 4.7");
    await expect(page.locator('meta[name="description"]')).toHaveAttribute(
      "content",
      /coding, AI agents, 1M context knowledge work/i
    );
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", "https://claudeopus47.lol/");
    await expect(page.locator('meta[property="og:site_name"]')).toHaveAttribute("content", "Claude Opus 4.7 Review");
    await expect(page.locator('meta[name="twitter:image:alt"]')).toHaveAttribute(
      "content",
      /editorial review cover graphic/i
    );
    await expect(page.locator('script[type="application/ld+json"]')).toHaveCount(4);

    await expect(page.getByRole("link", { name: "Read the Review" })).toBeVisible();
    await expect(page.getByRole("link", { name: "Jump to FAQ" })).toBeVisible();

    await page.getByRole("link", { name: "Read the Review" }).click();
    await expect(page.locator("#benchmarks")).toBeInViewport();

    await page.getByRole("link", { name: "Jump to FAQ" }).click();
    await expect(page.locator("#faq")).toBeInViewport();

    await expect(page.locator(".evidence-card")).toHaveCount(3);
    await expect(page.locator(".workflow-card")).toHaveCount(4);
    await expect(page.locator(".faq-list details")).toHaveCount(6);

    await page.locator(".faq-list details").nth(0).click();
    await expect(page.locator(".faq-list details").nth(0)).toHaveAttribute("open", "");

    const imagesLoaded = await page.evaluate(() =>
      Array.from(document.images).every((image) => image.complete && image.naturalWidth > 0)
    );
    expect(imagesLoaded).toBe(true);
  });

  test("mobile layout stays inside viewport and keeps key sections accessible", async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 390, height: 844 },
      isMobile: true
    });
    const page = await context.newPage();

    await page.goto("/");

    await expect(page.locator("h1")).toBeVisible();
    await expect(page.getByRole("link", { name: "Benchmarks" })).toBeVisible();

    await page.getByRole("link", { name: "Benchmarks" }).click();
    await expect(page.locator("#benchmarks")).toBeInViewport();

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);

    await expect(page.locator(".signal-card")).toHaveCount(4);
    await expect(page.locator(".score-card")).toHaveCount(4);

    await context.close();
  });
});
