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
                        Font = new Font("comic sans", 14)
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
            string[] lines = File.ReadAllLines(@"C:\takifolder\cardfile.txt");
            for (int i = 0; i < lines.Length; i++)                              // cards on hand
            {
                if (lines[i].Contains("_"))
                {
                    string[] components = lines[i].Substring(3).Split('_');
                    if (i == lines.Length - 1)
                    {
                        sign[1, 7].Text = components[0];
                        SetCardColor(cards[1, 7], components[1]);

                    }
                    else if (i < 7)
                    {
                        sign[0, i].Text = components[0];
                        SetCardColor(cards[0, i], components[1]);
                    }
                    else
                    {
                        sign[1, i - 7].Text = components[0];
                        SetCardColor(cards[1, i-7], components[1]);
                    }
                }
                else
                {
                    if (i < 7)
                        sign[0, i].Text = lines[i].Substring(3);
                    else
                        sign[1, i - 7].Text = lines[i].Substring(3);
                }
            }
        }
    }
}
