using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {

        private Panel[,] cards = new Panel[2, 8];
        private Label[,] sign = new Label[2, 8];
        private Label headline = new Label();
        private Label current = new Label();

        public Form1()
        {
            headline.Name = "headline";
            headline.Text = "Your cards";
            headline.Location = new Point(370, 20);
            headline.Size = new Size(300, 40);
            headline.Font = new Font("Comic Sans", 18);
            Controls.Add(headline);

            current.Name = "current card";
            current.Text = "Current card";
            current.Location = new Point(370, 330);
            current.Size = new Size(300, 40);
            current.Font = new Font("Comic Sans", 18);
            Controls.Add(current);

            for (int i = 0; i < 2; i++)
                for (int j = 0; j < 8; j++)
                {
                    if (i == 0 && j == 7)
                        continue;

                    cards[i, j] = new Panel();
                    if (i == 1 && j == 7)
                        cards[i, j].Location = new Point(400, 400);
                    else
                        cards[i, j].Location = new Point(j * 120 + 50, i * 120 + 70);

                    cards[i, j].Size = new Size(80, 100);
                    cards[i, j].BorderStyle = BorderStyle.FixedSingle;
                    cards[i, j].Name = i + "" + j;
                    Controls.Add(cards[i, j]);

                    sign[i, j] = new Label
                    {
                        Name = "sign " + i + "" + j,
                        Location = new Point(30, 40),
                        Font = new Font("comic sans", 16)
                    };
                    cards[i, j].Controls.Add(sign[i, j]);

                }
            InitializeComponent();
        }

        private void SetCardColor(Panel card, string color)
        {
            switch(color)
            {
                case "B":
                    card.BackColor = Color.DodgerBlue;
                    break;
                case "G":
                    card.BackColor = Color.LightGreen;
                    break;
                case "Y":
                    card.BackColor = Color.Gold;
                    break;
                case "R":
                    card.BackColor = Color.IndianRed;
                    break;

            }
        }

        private void fileSystemWatcher1_Changed_1(object sender, FileSystemEventArgs e)
        {
            bool isexists = false;
            string[] easycards = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "+"};
            string[] lines = File.ReadAllLines(@"C:\takifolder\cardfile.txt");
            for (int i = 0; i < lines.Length; i++)                              // cards on hand
            {
                for (int j = 0; j < easycards.Length; j++)
                    if (lines[i][3].ToString() == easycards[j])
                        isexists = true;

                if (isexists)
                {
                    string[] components = lines[i].Substring(3).Split('_');
                    if (i == lines.Length - 1)
                    {
                        cards[1, 7].Controls.Remove(sign[1, 7]);
                        sign[1, 7] = new Label();
                        if (components[0].Length > 1)
                            sign[1, 7].Location = new Point(25, 40);
                        else
                            sign[1, 7].Location = new Point(30, 40);
                        sign[1, 7].Text = components[0];
                        sign[1, 7].Font = new Font("comic sans", 16);
                        SetCardColor(cards[1, 7], components[1]);
                        cards[1, 7].Controls.Add(sign[1, 7]);

                    }
                    else if (i < 7)
                    {
                        cards[0, i].Controls.Remove(sign[0, i]);
                        sign[0, i] = new Label();
                        if (components[0].Length > 1)
                            sign[0, i].Location = new Point(25, 40);
                        else
                            sign[0, i].Location = new Point(30, 40);
                        sign[0, i].Text = components[0];
                        sign[0, i].Font = new Font("comic sans", 16);
                        
                        SetCardColor(cards[0, i], components[1]);
                        cards[0, i].Controls.Add(sign[0, i]);
                    }
                    else
                    {
                        cards[1, i - 7].Controls.Remove(sign[1, i - 7]);
                        sign[1, i - 7] = new Label();
                        if (components[0].Length > 1)
                            sign[1, i - 7].Location = new Point(25, 40);
                        else
                            sign[1, i - 7].Location = new Point(30, 40);
                        sign[1, i - 7].Text = components[0];
                        sign[1, i - 7].Font = new Font("comic sans", 16);
                        SetCardColor(cards[1, i - 7], components[1]);
                        cards[1, i - 7].Controls.Add(sign[1, i - 7]);
                    }
                }
                else
                {
                    if (i == lines.Length - 1)
                    {
                        cards[1, 7].Controls.Remove(sign[1, 7]);
                        sign[1, 7] = new Label();
                        cards[1, 7].BackColor = Color.White;
                        SetCardImage(sign[1, 7], lines[i]);
                        cards[1, 7].Controls.Add(sign[1, 7]);
                    }
                    else if (i < 7)
                    {
                        cards[0, i].Controls.Remove(sign[0, i]);
                        sign[0, i] = new Label();
                        cards[0, i].BackColor = Color.White;
                        SetCardImage(sign[0, i], lines[i]);
                        cards[0, i].Controls.Add(sign[0, i]);
                    }
                    else
                    {
                        cards[1, i - 7].Controls.Remove(sign[1, i - 7]);
                        sign[1, i - 7] = new Label();
                        cards[1, i - 7].BackColor = Color.White;
                        SetCardImage(sign[1, i - 7], lines[i]);
                        cards[1, i - 7].Controls.Add(sign[1, i - 7]);
                    }
                }
                isexists = false;
            }
        }

        public static void SetCardImage(Label sign, string cardtype)
        {
            sign.Location = new Point(2, 5);
            sign.Text = "";
            if (cardtype.Contains("cc"))
            {
                Image image = Image.FromFile(@"C:\Users\MAXIM\Desktop\taki\pics\change_color.png");
                sign.Image = image;
                sign.Size = new Size(image.Width, image.Height);
                

            }
            else if (cardtype.Contains("ct"))
            {
                Image image = Image.FromFile(@"C:\Users\MAXIM\Desktop\taki\pics\colorful_taki.png");
                sign.Image = image;
                sign.Size = new Size(image.Width, image.Height);
            }
            else
            {
                char cardcolor = cardtype[cardtype.Length - 1];
                string color = GetColorString(cardcolor);
                string path = @"C:\Users\MAXIM\Desktop\taki\pics\" + color + "_";
                char type = cardtype[3];
                switch(type)
                {
                    case '>':
                        path += "direct.png";
                        break;
                    case 'T':
                        path += "taki.png";
                        break;
                    case 'S':
                        path += "stop.png";
                        break;
                }
                Image image = Image.FromFile(path);
                sign.Image = image;
                sign.Size = new Size(image.Width, image.Height);
            }
        }
        public static string GetColorString(char letter)
        {
            switch (letter)
            {
                case 'B':
                    return "Blue";
                case 'G':
                    return "Green";
                case 'Y':
                    return "Yellow";
                case 'R':
                    return "Red";
            }
            return "white";
                
        }
    }
}
