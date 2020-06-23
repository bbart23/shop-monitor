using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using OpenQA;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;
using SeleniumExtras.PageObjects;
using SeleniumExtras.WaitHelpers;
using DiscordWebhookLib;
using Discord.Webhook;

namespace EZMonitor
{   
    class Program
    {
        //Variables//
        static List<SiteItem> ItemList = new List<SiteItem>();
        static string[] SupremeLinks = { "jackets", "shirts", "tops_sweaters", "sweatshirts", "pants", "shorts", "bags", "hats", "accessories", "shoes", "skate" };
        static IWebDriver driver, driver2;
        public static bool keepRunning = true;

        //Exit Events//
        //private delegate bool ConsoleCtrlHandlerDelegate(int sig);
        //[DllImport("Kernel32")]
        //private static extern bool SetConsoleCtrlHandler(ConsoleCtrlHandlerDelegate handler, bool add);
        //static ConsoleCtrlHandlerDelegate _consoleCtrlHandler;

        //Functions//
        static void ColorLine(string message, ConsoleColor color)
        {
            Console.ForegroundColor = color;
            Console.WriteLine(message);
            Console.ResetColor();
        }

        static bool ExistsInList(SiteItem item)
        {
            foreach(SiteItem Item in ItemList)
            {
                if(Item.Name == item.Name && Item.Color == item.Color)
                {
                    return true;
                }
            }
            return false;
        }

        private static bool IsElementPresent(IWebElement element)
        {
            try
            {
                element.FindElement(By.ClassName("sold_out_tag"));
                return true;
            }
            catch (NoSuchElementException)
            {
                return false;
            }
        }

        //static void CurrentDomain_ProcessExit(object sender, EventArgs e)
        //{
        //    driver.Quit();
        //    driver2.Quit();
        //}

        static void SendDiscordMessage(string itemName, string itemColor, string price, string availability, string url, string imageURL, string sizes, DiscordWebhookClient executor)
        {
            Discord.EmbedBuilder embed = new Discord.EmbedBuilder();
            embed.Title = itemName;
            embed.Description = "**Shop:** [Supreme (US)](https://www.supremenewyork.com/shop/)\n**Color:** " + itemColor + "\n**Price:** " + price + 
                "\n**State:** " + availability + "\n\n> QuickTask\n> ["+ sizes +"](" + url + ")";
            embed.Url = url;
            embed.Color = new Discord.Color(12726577);
            embed.Footer = new Discord.EmbedFooterBuilder().WithText("[SneakerAlpha]");
            embed.Timestamp = DateTime.Now;
            embed.ThumbnailUrl = imageURL;
            
            Discord.Embed message = embed.Build();
            List<Discord.Embed> embeds = new List<Discord.Embed> { message };
            executor.SendMessageAsync(null, false, embeds, "Sneaker Alpha");
        }

        static void Main(string[] args)
        {
            //EXIT HANDLER//
            //_consoleCtrlHandler += s =>
            //{
            //    driver.Quit();
            //    return false;
            //};
            //SetConsoleCtrlHandler(_consoleCtrlHandler, true);

            string dir = @"C:\temp";
            string serializationFile = Path.Combine(dir, "items.bin");

            Console.CancelKeyPress += delegate
            {
                Console.WriteLine("Quitting Drivers...");
                driver.Quit();
                driver2.Quit();
                Console.WriteLine("Saving to File...");
                using (Stream stream = File.Open(serializationFile, FileMode.Create))
                {
                    var bformatter = new System.Runtime.Serialization.Formatters.Binary.BinaryFormatter();
                    bformatter.Serialize(stream, ItemList);
                }
                return;
            };

            //CHROME SETTINGS//
            ChromeOptions options = new ChromeOptions();
            options.AddArgument("headless"); //windowless
            options.AddUserProfilePreference("profile.default_content_setting_values.images", 2); //no images
            var chromeDriverService = ChromeDriverService.CreateDefaultService();
            chromeDriverService.HideCommandPromptWindow = true;

            driver = new ChromeDriver("C:/Users/Brandon/Downloads/chromedriver_win32/", options);
            driver2 = new ChromeDriver("C:/Users/Brandon/Downloads/chromedriver_win32/", options);
            string jacketsHook, shirtsHook, topsHook, sweatshirtsHook, pantsHook, shortsHook, hatsHook, bagsHook, accessoriesHook, shoesHook, skateHook;
            jacketsHook = "https://discordapp.com/api/webhooks/720718856334737461/QY7tsbDCROQsJbmJKHSpYo8cZkHd6A8xwKGY1r1mFLFzboxCatATfM23ivHSF5Dxtf3l";
            shirtsHook = "https://discordapp.com/api/webhooks/720718993509449841/g1MM58AwvkDAM1DTQKwc0CA4X_NIjbdTm7qDyJsNgdwUFsuHDq4Fc2QPwK-xd-zjPnX_";
            topsHook = "https://discordapp.com/api/webhooks/720719064850366545/02kPtBhlKNzeZIloPPf3qp4A-leg-EE45PGHvDtN8p7noZd27yCq28XXkqAlzmuTbFhB";
            sweatshirtsHook = "https://discordapp.com/api/webhooks/720719283348439111/h_6peoDUdU9qTavCpANm4tLh4V-s_2bH4fGhMQEGQm6BgxmLgK_ZWjClmwKbx7aX0uEE";
            pantsHook = "https://discordapp.com/api/webhooks/720719348490174575/qdLqBGZHA0XpdAm0bSxjuy0txqbrNPsm1t9uvQAmfhmxsD4TSp-Y6gzI5xcqz4__HBK7";
            shortsHook = "https://discordapp.com/api/webhooks/720719480820334684/OTAxO0gj4v6lpaV7Ws_aWT4dnYVBrQrnHSHXsSk_XoAMX2Q93r81FnhGpLPwNtRne804";
            hatsHook = "https://discordapp.com/api/webhooks/720719572373864478/mndahLkPYwZ3YtUW94dSNVmqZ9uwEoykbJsgbvtyMighEIolw_n6edOGEbQtnJanIvuF";
            bagsHook = "https://discordapp.com/api/webhooks/720719634474598552/HM86d8z9H1WhBiK4RLRvAZ11Hcq5BPIrKfoT2ZKFoltcmdON2nKpArWbEb_mkOZjbx0h";
            accessoriesHook = "https://discordapp.com/api/webhooks/720719983390359693/w68pRsUksEpEXArI2fj4GxRjL3IypM0SfUVDzN024lGxY1HJiIMknOF_BNq640CmhcMQ";
            shoesHook = "https://discordapp.com/api/webhooks/720720113371840534/XA-1s3t1ynsq-1FW9WLylvgHIOk-QbK21qJUBWfitvwauuaRFYkQ5Q54bNnZs_2zFhGi";
            skateHook = "https://discordapp.com/api/webhooks/720720159333023815/IuZzeFJgK0gc2bjKMjTTkRe9ZlEZmLeGfdJLzCs1lAEbTEKlsOqJDj7gNe8EeVR2z9ae";
            Discord.Webhook.DiscordWebhookClient executor = new DiscordWebhookClient(jacketsHook);
            DiscordWebhookClient jackets = new DiscordWebhookClient(jacketsHook);
            DiscordWebhookClient shirts = new DiscordWebhookClient(shirtsHook);
            DiscordWebhookClient tops = new DiscordWebhookClient(topsHook);
            DiscordWebhookClient sweatshirts = new DiscordWebhookClient(sweatshirtsHook);
            DiscordWebhookClient pants = new DiscordWebhookClient(pantsHook);
            DiscordWebhookClient shorts = new DiscordWebhookClient(shortsHook);
            DiscordWebhookClient hats = new DiscordWebhookClient(hatsHook);
            DiscordWebhookClient bags = new DiscordWebhookClient(bagsHook);
            DiscordWebhookClient accessories = new DiscordWebhookClient(accessoriesHook);
            DiscordWebhookClient shoes = new DiscordWebhookClient(shoesHook);
            DiscordWebhookClient skate = new DiscordWebhookClient(skateHook);

            while (true)
            {
                foreach(string supremelink in SupremeLinks)
                {
                    switch (supremelink)
                    {
                        case "jackets":
                            executor = jackets; break;
                        case "shirts":
                            executor = shirts; break;
                        case "tops_sweaters":
                            executor = tops; break;
                        case "sweatshirts":
                            executor = sweatshirts; break;
                        case "pants":
                            executor = pants; break;
                        case "shorts":
                            executor = shorts; break;
                        case "hats":
                            executor = hats; break;
                        case "bags":
                            executor = bags; break;
                        case "accessories":
                            executor = accessories; break;
                        case "shoes":
                            executor = shoes; break;
                        case "skate":
                            executor = skate; break;
                        default:
                            break;
                    }
                    driver.Navigate().GoToUrl("https://supremenewyork.com/shop/all/" + supremelink);
                    TimeSpan span = new TimeSpan(0, 0, 100);
                    WebDriverWait some_element = new WebDriverWait(driver, span);
                    WebDriverWait some_element2 = new WebDriverWait(driver2, span);
                    Console.WriteLine("Waiting for page load");
                    some_element.Until(SeleniumExtras.WaitHelpers.ExpectedConditions.VisibilityOfAllElementsLocatedBy(By.Id("container")));
                    Console.WriteLine("Viewing " + supremelink);
                    var Container = driver.FindElement(By.Id("container"));
                    foreach (var article in Container.FindElements(By.ClassName("inner-article")))
                    {
                        //Console.WriteLine("Finding Item...");
                        var ItemName = article.FindElement(By.ClassName("product-name")).FindElement(By.ClassName("name-link")).Text;
                        Console.WriteLine("Item Name: " + ItemName);
                        var ItemColor = article.FindElement(By.ClassName("product-style")).FindElement(By.ClassName("name-link")).Text;
                        bool SoldOut = IsElementPresent(article);
                        var ItemLink = article.FindElement(By.TagName("a")).GetAttribute("href");
                        var ItemPicture = article.FindElement(By.TagName("img")).GetAttribute("src");
                        Console.WriteLine(ItemPicture);
                        


                        SiteItem temp = new SiteItem(ItemName, ItemColor, SoldOut);
                        if(ExistsInList(temp))
                        {
                            int index = ItemList.FindIndex(a => a.Name == ItemName && a.Color == ItemColor);
                            bool oldSoldOut = ItemList[index].SoldOut;
                            string oldPrice = ItemList[index].Price;
                            string oldSizes = ItemList[index].Sizes;

                            if (SoldOut != oldSoldOut)
                            {
                                ItemList.RemoveAt(index);
                                ItemList.Add(temp);
                                if(!SoldOut)
                                {
                                    driver2.Navigate().GoToUrl(ItemLink);
                                    Console.WriteLine(ItemLink);
                                    Console.WriteLine("Waiting for price");
                                    some_element2.Until(SeleniumExtras.WaitHelpers.ExpectedConditions.VisibilityOfAllElementsLocatedBy(By.Id("container")));
                                    Console.WriteLine("Done");
                                    var ItemPrice = driver2.FindElement(By.ClassName("price")).Text;
                                    temp.Price = ItemPrice;
                                    var sizeString = "";
                                    foreach (var size in driver2.FindElement(By.Id("cctrl")).FindElements(By.TagName("option")))
                                    {
                                        if (sizeString == "")
                                        {
                                            sizeString += size.Text;
                                        }
                                        else
                                            sizeString += "|" + size.Text;
                                    }

                                    temp.Sizes = sizeString;
                                    ColorLine("[RESTOCK] [" + DateTime.Now + "] " + ItemName + " " + ItemColor, ConsoleColor.Green);
                                    SendDiscordMessage(ItemName, ItemColor, ItemPrice, "RESTOCK", ItemLink, ItemPicture, sizeString, executor);
                                    //executor.SendMessageAsync("[RESTOCK] [" + DateTime.Now + "] " + ItemName + " " + ItemColor + "Link: " + ItemLink, false, null, "Sneaker Alpha");
                                }
                                else
                                {
                                    SendDiscordMessage(ItemName, ItemColor, oldPrice, "Sold Out", ItemLink, ItemPicture, oldSizes, executor);
                                    ColorLine("[SOLD OUT]" + ItemName + " " + ItemColor, ConsoleColor.Red);
                                }
                            }
                        }
                        else
                        {
                            driver2.Navigate().GoToUrl(ItemLink);
                            Console.WriteLine(ItemLink);
                            Console.WriteLine("Waiting for price");
                            some_element2.Until(SeleniumExtras.WaitHelpers.ExpectedConditions.VisibilityOfAllElementsLocatedBy(By.Id("container")));
                            Console.WriteLine("Done");
                            var ItemPrice = driver2.FindElement(By.ClassName("price")).Text;
                            temp.Price = ItemPrice;
                            var sizeString = "";
                            foreach(var size in driver2.FindElement(By.Id("cctrl")).FindElements(By.TagName("option")))
                            {
                                if (sizeString == "")
                                {
                                    sizeString += size.Text;
                                }
                                else 
                                    sizeString += "|" + size.Text;
                            }
                 
                            temp.Sizes = sizeString;
                            if (!SoldOut)
                            {
                                SendDiscordMessage(ItemName, ItemColor, ItemPrice, "In Stock", ItemLink, ItemPicture, sizeString, executor);
                            }
                            
                            //executor.SendMessageAsync("[Item] " + ItemName + " " + ItemColor + " " + SoldOut.ToString(), false, null, "Sneaker Alpha");
                            Console.WriteLine("[Item] " + ItemName + " " + ItemColor + " " + SoldOut.ToString());
                            ItemList.Add(temp);
                        }
                    }
                }                  
            }
        }
    }
}
